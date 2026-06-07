"""State definitions for the customer care workflow.

This module defines the shared workflow state and supporting type
aliases used by the customer care agent.

The state is represented as a TypedDict and is passed between workflow
nodes during execution. It stores customer information, issue
classification results, SQL knowledge lookups, ticketing data,
human-review decisions, routing information, and the final response.

Type aliases are provided for constrained values such as issue
categories, priority levels, and workflow actions to improve type
safety and maintainability.
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

Priority = Literal[
    "low",
    "medium",
    "high",
    "critical",
]

NextAction = Literal[
    "known_resolution",
    "create_ticket",
    "human_review",
    "final_response",
]


class CustomerCareState(TypedDict, total=False):
    """Represents the shared state of a customer care workflow.

    The state object is incrementally populated as the workflow
    progresses through understanding, classification, knowledge
    retrieval, ticket creation, human review, and response generation.

    Attributes:
        customer_email: Customer email address.
        customer_name: Customer name.
        product_hint: Product identifier provided by the customer.
        complaint_text: Original customer complaint.
        channel: Communication channel (email, chat, phone, etc.).

        issue_summary: Generated summary of the issue.
        detected_product: Product identified from the complaint.
        customer_intent: Detected customer intent.

        category: Classified issue category.
        priority: Assigned priority level.
        seriousness_reason: Reason for the assigned priority.
        escalation_required: Indicates whether escalation is required.

        sql_answer: Information retrieved from the knowledge database.
        known_resolution_found: Indicates whether a matching resolution
            was found.
        known_resolution: Retrieved resolution text.
        similar_ticket: Reference to a similar historical ticket.

        ticket_required: Indicates whether a support ticket should be
            created.
        ticket_id: Internal ticket identifier.
        ticket_ref: Customer-facing ticket reference.
        assigned_agent_email: Email address of the assigned support
            agent.

        human_review_required: Indicates whether manual review is
            required.
        human_decision: Decision provided during manual review.
        human_comments: Additional reviewer comments.

        next_action: Next workflow action to execute.

        response: Final response to be sent to the customer.
        debug: Debugging and trace information.
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

    # SQL Knowledge
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