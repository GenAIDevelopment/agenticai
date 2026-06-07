"""Unit tests for the deterministic workflow logic.

These cover ``classify_complaint``, ``decide_next_action`` and
``route_after_decision`` in isolation — no LLM or database involved.
"""

import pytest

from nodes import classify_complaint, decide_next_action, route_after_decision


@pytest.mark.parametrize(
    ("complaint", "expected_category", "expected_priority"),
    [
        ("My TV is not working and has a dead pixel", "product_defect", "high"),
        ("I want to claim warranty replacement", "warranty_claim", "high"),
        ("I need help with installation and setup", "installation_support", "medium"),
        ("Bluetooth pairing fails after the firmware update", "software_issue", "medium"),
        ("My order arrived with a cracked screen", "shipping_damage", "critical"),
        ("I want a refund / money back", "returns_refunds", "high"),
        ("My invoice shows I was charged twice", "billing", "medium"),
        ("Just a general question about your store", "general_inquiry", "medium"),
    ],
)
def test_classify_complaint_categories(complaint, expected_category, expected_priority):
    """Each complaint keyword set maps to the expected category and priority."""
    result = classify_complaint({"complaint_text": complaint})
    assert result["category"] == expected_category
    assert result["priority"] == expected_priority


def test_classify_complaint_escalation_language():
    """Serious grievance language sets escalation, review and critical priority."""
    state = {
        "complaint_text": "I complained many times and will go to consumer court",
    }
    result = classify_complaint(state)
    assert result["escalation_required"] is True
    assert result["human_review_required"] is True
    assert result["priority"] == "critical"
    assert result["seriousness_reason"]


def test_classify_complaint_no_escalation_by_default():
    """An ordinary complaint does not trigger escalation or human review."""
    result = classify_complaint({"complaint_text": "My headphones will not pair"})
    assert result["escalation_required"] is False
    assert result["human_review_required"] is False


def test_decide_next_action_human_review_wins():
    """Escalation takes precedence over an available known resolution."""
    state = {"escalation_required": True, "known_resolution_found": True}
    assert decide_next_action(state)["next_action"] == "human_review"


def test_decide_next_action_critical_priority_triggers_review():
    """Critical priority alone routes to human review."""
    state = {"priority": "critical", "known_resolution_found": True}
    assert decide_next_action(state)["next_action"] == "human_review"


def test_decide_next_action_known_resolution():
    """A known resolution (no escalation) routes to the resolution response."""
    state = {"known_resolution_found": True}
    assert decide_next_action(state)["next_action"] == "known_resolution"


def test_decide_next_action_create_ticket_fallback():
    """With no escalation and no known resolution, the default is ticket creation."""
    state = {"known_resolution_found": False}
    assert decide_next_action(state)["next_action"] == "create_ticket"


@pytest.mark.parametrize(
    "next_action", ["known_resolution", "create_ticket", "human_review"]
)
def test_route_after_decision_returns_next_action(next_action):
    """The router echoes the ``next_action`` value for the conditional edge."""
    assert route_after_decision({"next_action": next_action}) == next_action
