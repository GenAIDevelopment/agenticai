"""Workflow nodes for the customer care LangGraph.

Each node receives the shared :class:`~state.CustomerCareState` and returns a
partial update. The flow is:

    understand_complaint -> sql_knowledge_node -> classify_complaint
    -> decide_next_action -> (known_resolution | create_ticket | human_review)
    -> response node -> END

All customer-facing text is written to the ``response`` state key.
"""

from langgraph.types import interrupt

from state import CustomerCareState
from sql_agent_service import ask_database
from ticket_repository import create_ticket


def understand_complaint(state: CustomerCareState) -> CustomerCareState:
    """Summarize the complaint and detect the referenced product.

    This MVP implementation uses simple rules: it truncates the complaint to a
    short summary and treats the supplied product hint as the detected product.

    Args:
        state: Current workflow state; must contain ``complaint_text``.

    Returns:
        CustomerCareState: State updated with ``issue_summary`` and
        ``detected_product``.
    """
    complaint = state["complaint_text"]
    product_hint = state.get("product_hint")

    detected_product = product_hint
    issue_summary = complaint.strip()[:300]

    return {
        **state,
        "issue_summary": issue_summary,
        "detected_product": detected_product,
        "debug": {
            **state.get("debug", {}),
            "understand_complaint": "Complaint summarized",
        },
    }


def sql_knowledge_node(state: CustomerCareState) -> CustomerCareState:
    """Ask the read-only SQL agent whether this is a known, resolved issue.

    Builds a natural-language question from the complaint and product hint,
    sends it to :func:`sql_agent_service.ask_database`, and records whether a
    known resolution was found.

    Args:
        state: Current workflow state; must contain ``complaint_text``.

    Returns:
        CustomerCareState: State updated with ``sql_answer``,
        ``known_resolution_found`` and ``known_resolution``.
    """
    complaint = state["complaint_text"]
    product_hint = state.get("product_hint") or "not provided"

    question = f"""
A customer has the following complaint:

Complaint:
{complaint}

Product hint:
{product_hint}

Find whether this is a known issue with a known resolution.

Use the database tables and views.
Look for:
- matching product
- similar resolved tickets
- resolution summary
- root cause
- action taken

Return:
known_resolution_found: yes/no
similar_ticket_ref: value if available
known_resolution: short practical answer for customer
support_notes: short internal notes
"""

    answer = ask_database(question)
    known_resolution_found = "known_resolution_found: yes" in answer.lower()

    return {
        **state,
        "sql_answer": answer,
        "known_resolution_found": known_resolution_found,
        "known_resolution": answer if known_resolution_found else None,
        "debug": {
            **state.get("debug", {}),
            "sql_knowledge_node": answer,
        },
    }


def classify_complaint(state: CustomerCareState) -> CustomerCareState:
    """Classify the complaint into a database enum category and a priority.

    Applies keyword rules to derive the ``category`` and ``priority`` and flags
    escalation when the text contains serious grievance language.

    Args:
        state: Current workflow state; must contain ``complaint_text``.

    Returns:
        CustomerCareState: State updated with ``category``, ``priority``,
        ``escalation_required``, ``human_review_required`` and
        ``seriousness_reason``.
    """
    text = state["complaint_text"].lower()

    category = "general_inquiry"
    priority = "medium"
    escalation_required = False
    seriousness_reason = None

    if any(
        word in text
        for word in [
            "not working",
            "defect",
            "broken",
            "dead pixel",
            "overheating",
            "not detected",
        ]
    ):
        category = "product_defect"
        priority = "high"

    if any(word in text for word in ["warranty", "replacement", "guarantee"]):
        category = "warranty_claim"
        priority = "high"

    if any(word in text for word in ["install", "installation", "setup", "mount"]):
        category = "installation_support"
        priority = "medium"

    if any(
        word in text
        for word in [
            "software",
            "firmware",
            "update",
            "bluetooth",
            "pairing",
            "app",
            "driver",
        ]
    ):
        category = "software_issue"
        priority = "medium"

    if any(
        word in text
        for word in [
            "cracked",
            "shipping damage",
            "damaged delivery",
            "delivered damaged",
        ]
    ):
        category = "shipping_damage"
        priority = "critical"

    if any(word in text for word in ["return", "refund", "money back"]):
        category = "returns_refunds"
        priority = "high"

    if any(
        word in text
        for word in ["invoice", "billing", "charged", "payment", "amount deducted"]
    ):
        category = "billing"
        priority = "medium"

    serious_words = [
        "consumer court",
        "legal",
        "police",
        "fraud",
        "repeated",
        "many times",
        "third time",
        "business loss",
        "urgent escalation",
    ]

    if any(word in text for word in serious_words):
        priority = "critical"
        escalation_required = True
        seriousness_reason = "Customer complaint contains serious escalation language."

    return {
        **state,
        "category": category,
        "priority": priority,
        "escalation_required": escalation_required,
        "human_review_required": escalation_required,
        "seriousness_reason": seriousness_reason,
        "debug": {
            **state.get("debug", {}),
            "classify_complaint": {
                "category": category,
                "priority": priority,
                "escalation_required": escalation_required,
            },
        },
    }


def decide_next_action(state: CustomerCareState) -> CustomerCareState:
    """Decide the routing target for the workflow.

    Escalation or critical priority routes to human review; otherwise a known
    resolution short-circuits to a direct response, and everything else creates
    a ticket.

    Args:
        state: Current workflow state.

    Returns:
        CustomerCareState: State updated with ``next_action`` (one of
        ``"human_review"``, ``"known_resolution"`` or ``"create_ticket"``).
    """
    if state.get("escalation_required") or state.get("priority") == "critical":
        next_action = "human_review"
    elif state.get("known_resolution_found"):
        next_action = "known_resolution"
    else:
        next_action = "create_ticket"

    return {
        **state,
        "next_action": next_action,
        "debug": {
            **state.get("debug", {}),
            "decide_next_action": next_action,
        },
    }


def route_after_decision(state: CustomerCareState) -> str:
    """Return the branch to follow after ``decide_next_action``.

    Args:
        state: Current workflow state; must contain ``next_action``.

    Returns:
        str: The value of ``next_action``, used by the conditional edge.
    """
    return state["next_action"]


def create_ticket_node(state: CustomerCareState) -> CustomerCareState:
    """Create a support ticket via the safe repository.

    Delegates to :func:`ticket_repository.create_ticket` and stores the
    returned identifiers on the state.

    Args:
        state: Current workflow state; must contain ``complaint_text``.

    Returns:
        CustomerCareState: State updated with ``ticket_id``, ``ticket_ref`` and
        ``assigned_agent_email``.
    """
    ticket = create_ticket(
        customer_email=state.get("customer_email"),
        product_hint=state.get("product_hint"),
        complaint_text=state["complaint_text"],
        channel=state.get("channel", "chat"),
        category=state.get("category", "general_inquiry"),
        priority=state.get("priority", "medium"),
    )

    return {
        **state,
        "ticket_required": False,
        "ticket_id": ticket["ticket_id"],
        "ticket_ref": ticket["ticket_ref"],
        "assigned_agent_email": ticket["assigned_agent_email"],
        "debug": {
            **state.get("debug", {}),
            "create_ticket_node": ticket,
        },
    }


def human_review_node(state: CustomerCareState) -> CustomerCareState:
    """Pause the graph for human review of a serious grievance.

    Calls :func:`langgraph.types.interrupt`, which suspends execution and
    persists state via the checkpointer until resumed with
    ``Command(resume=...)``. The resume value is expected to provide
    ``decision`` and ``comments``.

    Args:
        state: Current workflow state.

    Returns:
        CustomerCareState: State updated with ``human_decision`` and
        ``human_comments`` once the workflow is resumed.
    """
    review_payload = {
        "reason": state.get("seriousness_reason"),
        "category": state.get("category"),
        "priority": state.get("priority"),
        "complaint_text": state.get("complaint_text"),
        "sql_findings": state.get("sql_answer"),
        "suggested_action": "Approve critical ticket creation and escalation.",
    }

    decision = interrupt(review_payload)

    return {
        **state,
        "human_decision": decision.get("decision"),
        "human_comments": decision.get("comments"),
        "debug": {
            **state.get("debug", {}),
            "human_review_node": decision,
        },
    }


def known_resolution_response_node(state: CustomerCareState) -> CustomerCareState:
    """Build a customer-facing response for a known, resolved issue.

    Args:
        state: Current workflow state; expects ``known_resolution``.

    Returns:
        CustomerCareState: State updated with ``response``.
    """
    response = f"""
I found a similar known issue and resolution.

{state.get("known_resolution")}

If this does not solve your issue, please ask me to create a support ticket.
""".strip()

    return {
        **state,
        "response": response,
    }


def ticket_created_response_node(state: CustomerCareState) -> CustomerCareState:
    """Build a customer-facing response after a ticket is created.

    Uses an escalation-flavoured message when the ticket came from the human
    review path (``human_decision`` is set), otherwise a standard confirmation.

    Args:
        state: Current workflow state; expects ``ticket_ref``, ``category`` and
            ``priority``.

    Returns:
        CustomerCareState: State updated with ``response``.
    """
    if state.get("human_decision"):
        response = f"""
Your grievance has been reviewed and registered as a critical support case.

Ticket Reference: {state.get("ticket_ref")}
Category: {state.get("category")}
Priority: {state.get("priority")}
Assigned Agent: {state.get("assigned_agent_email")}
Human Review Decision: {state.get("human_decision")}
Reviewer Comments: {state.get("human_comments")}

A senior support representative will handle this case.
""".strip()
    else:
        response = f"""
Your support ticket has been created.

Ticket Reference: {state.get("ticket_ref")}
Category: {state.get("category")}
Priority: {state.get("priority")}
Assigned Agent: {state.get("assigned_agent_email")}

Our support team will review this and get back to you.
""".strip()

    return {
        **state,
        "response": response,
    }
