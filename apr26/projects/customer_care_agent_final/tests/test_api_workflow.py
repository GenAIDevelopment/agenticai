"""End-to-end tests for the FastAPI endpoints driving the LangGraph workflow.

The real graph runs; only the Gemini SQL agent (``nodes.ask_database``) and the
PostgreSQL write (``nodes.create_ticket``) are faked via fixtures in
``conftest.py``. This validates routing, the interrupt/resume cycle, and the
HTTP request/response shapes without external services.
"""

import nodes

KNOWN_RESOLUTION_ANSWER = (
    "known_resolution_found: yes\n"
    "similar_ticket_ref: TKT-2024-00002\n"
    "known_resolution: Re-pair the headphones by holding the power button for 7 seconds.\n"
    "support_notes: common Bluetooth pairing issue"
)


def test_health_check(client):
    """``GET /`` returns the liveness payload."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_known_issue_returns_resolution_without_ticket(client, monkeypatch, created_tickets):
    """A known resolution is returned to the customer and no ticket is created."""
    # Simulate the SQL agent finding a known resolution.
    monkeypatch.setattr(nodes, "ask_database", lambda question: KNOWN_RESOLUTION_ANSWER)

    response = client.post(
        "/api/v1/complaints",
        json={
            "customer_email": "sneha.reddy@email.com",
            "product_hint": "Sony WH-1000XM5",
            "complaint_text": "My Sony WH-1000XM5 headphones are not pairing with my Dell laptop.",
            "channel": "chat",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["interrupted"] is False
    assert body["ticket_ref"] is None
    assert "known issue and resolution" in body["response"]
    # No ticket should be created for a known issue.
    assert created_tickets == []


def test_new_issue_creates_ticket(client, created_tickets):
    """An unknown issue creates exactly one ticket and confirms it to the customer."""
    # Default fixture: ask_database reports no known resolution.
    response = client.post(
        "/api/v1/complaints",
        json={
            "customer_email": "rahul.mehta@email.com",
            "product_hint": "Samsung T7 SSD",
            "complaint_text": "My Samsung T7 Portable SSD is not detected on Windows 11.",
            "channel": "chat",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["interrupted"] is False
    assert body["ticket_ref"] == "TKT-TEST-00999"
    assert "support ticket has been created" in body["response"]

    # Exactly one ticket created, classified as a product defect.
    assert len(created_tickets) == 1
    assert created_tickets[0]["category"] == "product_defect"
    assert created_tickets[0]["priority"] == "high"


def test_serious_grievance_interrupts_for_human_review(client, created_tickets):
    """A serious grievance pauses for human review without creating a ticket."""
    response = client.post(
        "/api/v1/complaints",
        json={
            "customer_email": "vikram.patel@email.com",
            "product_hint": "iPad Pro",
            "complaint_text": (
                "My iPad Pro arrived with a cracked screen. "
                "I complained many times and will go to consumer court."
            ),
            "channel": "email",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "human_review_required"
    assert body["interrupted"] is True
    assert body["thread_id"]
    assert body["review_payload"] is not None
    # The graph paused before creating a ticket.
    assert created_tickets == []


def test_serious_grievance_resume_creates_ticket(client, created_tickets):
    """Approving a paused grievance resumes the graph and creates a critical ticket."""
    # 1. Submit a serious grievance -> graph interrupts.
    submit = client.post(
        "/api/v1/complaints",
        json={
            "customer_email": "vikram.patel@email.com",
            "product_hint": "iPad Pro",
            "complaint_text": (
                "My iPad Pro arrived with a cracked screen. "
                "I complained many times and will go to consumer court."
            ),
            "channel": "email",
        },
    )
    thread_id = submit.json()["thread_id"]
    assert submit.json()["status"] == "human_review_required"

    # 2. Reviewer approves -> resume the same thread.
    resume = client.post(
        f"/api/v1/reviews/{thread_id}/resume",
        json={
            "decision": "approve_escalation",
            "comments": "Valid serious grievance. Create critical ticket and escalate.",
        },
    )

    assert resume.status_code == 200
    body = resume.json()
    assert body["status"] == "resumed"
    assert body["ticket_ref"] == "TKT-TEST-00999"
    assert "critical support case" in body["response"]
    assert "approve_escalation" in body["response"]

    # A critical ticket was created after approval.
    assert len(created_tickets) == 1
    assert created_tickets[0]["priority"] == "critical"
    assert created_tickets[0]["category"] == "shipping_damage"


def test_unknown_thread_resume_returns_404(client):
    """Resuming a thread that never interrupted returns a clean 404, not a 500."""
    # Resuming a thread that never interrupted returns a clean 404, not a 500.
    resume = client.post(
        "/api/v1/reviews/does-not-exist/resume",
        json={"decision": "approve_escalation", "comments": "n/a"},
    )
    assert resume.status_code == 404
    assert "No interrupted workflow" in resume.json()["detail"]
