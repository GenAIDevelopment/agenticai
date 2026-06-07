"""FastAPI entry point exposing the customer care LangGraph workflow.

Endpoints:
  * ``GET  /``                                  - health check
  * ``POST /api/v1/complaints``                 - submit a complaint
  * ``POST /api/v1/reviews/{thread_id}/resume`` - resume after human review

Run with::

    uv run fastapi dev main.py

then open http://127.0.0.1:8000/docs.
"""

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from langgraph.types import Command

from graph import customer_care_graph
from schemas import ComplaintRequest, ComplaintResponse, HumanReviewRequest

app = FastAPI(title="Customer Care LangGraph Agent")


@app.get("/")
def health_check():
    """Report service liveness.

    Returns:
        dict: ``{"status": "ok"}``.
    """
    return {"status": "ok"}


@app.post("/api/v1/complaints", response_model=ComplaintResponse)
def submit_complaint(request: ComplaintRequest):
    """Process a customer complaint through the workflow.

    Args:
        request: Parsed complaint payload.

    Returns:
        ComplaintResponse: A completed response (known resolution or created
        ticket), or a ``human_review_required`` signal carrying the interrupt
        payload and the ``thread_id`` needed to resume.
    """
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "customer_email": request.customer_email,
        "customer_name": request.customer_name,
        "product_hint": request.product_hint,
        "complaint_text": request.complaint_text,
        "channel": request.channel,
        "known_resolution_found": False,
        "ticket_required": True,
        "escalation_required": False,
        "human_review_required": False,
        "debug": {},
    }

    result = customer_care_graph.invoke(initial_state, config=config)

    if "__interrupt__" in result:
        return ComplaintResponse(
            thread_id=thread_id,
            status="human_review_required",
            interrupted=True,
            review_payload=result["__interrupt__"],
        )

    return ComplaintResponse(
        thread_id=thread_id,
        status="completed",
        response=result.get("response"),
        ticket_ref=result.get("ticket_ref"),
        interrupted=False,
    )


@app.post("/api/v1/reviews/{thread_id}/resume")
def resume_review(thread_id: str, request: HumanReviewRequest):
    """Resume an interrupted workflow with the reviewer's decision.

    Args:
        thread_id: Identifier of the paused workflow (from the submit response).
        request: Reviewer decision and optional comments.

    Returns:
        dict: ``status``, the final ``response``, the ``ticket_ref`` and the
        per-node ``debug`` trace.

    Raises:
        HTTPException: 404 if ``thread_id`` has no workflow paused for review
            (unknown thread, or one that already completed).
    """
    config = {"configurable": {"thread_id": thread_id}}

    snapshot = customer_care_graph.get_state(config)
    if not snapshot.next:
        raise HTTPException(
            status_code=404,
            detail="No interrupted workflow found for this thread_id.",
        )

    result = customer_care_graph.invoke(
        Command(
            resume={
                "decision": request.decision,
                "comments": request.comments,
            }
        ),
        config=config,
    )

    return {
        "status": "resumed",
        "response": result.get("response"),
        "ticket_ref": result.get("ticket_ref"),
        "debug": result.get("debug"),
    }
