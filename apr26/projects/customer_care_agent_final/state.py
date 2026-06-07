"""LangGraph state definition for the customer care workflow.

LangGraph is state-based: every node receives the shared state and returns
a partial update. ``CustomerCareState`` holds all information that flows
through the graph, from the raw complaint to the final customer response.
"""

from typing import Any, Literal, Optional, TypedDict

Category = Literal[
    "product_defect",
    "warranty_claim",
    "installation_support",
    "software_issue",
    "shipping_damage",
    "returns_refunds",
    "billing",
    "general_inquiry",
]

Priority = Literal["low", "medium", "high", "critical"]

NextAction = Literal[
    "known_resolution",
    "create_ticket",
    "human_review",
    "final_response",
]


class CustomerCareState(TypedDict, total=False):
    """Mutable state shared across all customer care graph nodes.

    Every node receives this mapping and returns a partial update that is merged
    back in. ``total=False`` means all keys are optional; nodes populate them as
    the workflow progresses. Keys are grouped (see inline comments) into: input,
    understanding, classification, SQL knowledge, ticket, human review, routing
    and final-response fields.

    Attributes:
        complaint_text: The raw customer complaint (the only required input).
        category: Classified ticket category (see :data:`Category`).
        priority: Assigned ticket priority (see :data:`Priority`).
        next_action: Routing decision (see :data:`NextAction`).
        ticket_ref: Customer-facing ticket reference once a ticket is created.
        response: Final customer-facing reply produced by a response node.
        debug: Per-node trace accumulated for observability.
    """

    # Input
    customer_email: Optional[str]
    customer_name: Optional[str]
    product_hint: Optional[str]
    complaint_text: str
    channel: str

    # Understanding
    issue_summary: Optional[str]
    detected_product: Optional[str]
    customer_intent: Optional[str]

    # Classification
    category: Optional[Category]
    priority: Optional[Priority]
    seriousness_reason: Optional[str]
    escalation_required: bool

    # SQL knowledge
    sql_answer: Optional[str]
    known_resolution_found: bool
    known_resolution: Optional[str]
    similar_ticket: Optional[str]

    # Ticket
    ticket_required: bool
    ticket_id: Optional[int]
    ticket_ref: Optional[str]
    assigned_agent_email: Optional[str]

    # Human review
    human_review_required: bool
    human_decision: Optional[str]
    human_comments: Optional[str]

    # Routing
    next_action: Optional[NextAction]

    # Final
    response: Optional[str]
    debug: dict[str, Any]
