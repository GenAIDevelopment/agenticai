"""Pydantic request/response models for the FastAPI layer.

These models define and validate the JSON shapes accepted and returned by the
endpoints in :mod:`main`.
"""

from pydantic import BaseModel


class ComplaintRequest(BaseModel):
    """Incoming customer complaint.

    Attributes:
        customer_email: Customer email address, if known.
        customer_name: Customer name, if known.
        product_hint: Product name or hint supplied by the customer.
        complaint_text: Free-text complaint (required).
        channel: Channel the complaint arrived on; defaults to ``"chat"``.
    """

    customer_email: str | None = None
    customer_name: str | None = None
    product_hint: str | None = None
    complaint_text: str
    channel: str = "chat"


class ComplaintResponse(BaseModel):
    """Result of processing a complaint, or a pending human-review signal.

    Attributes:
        thread_id: Workflow thread identifier, needed to resume after review.
        status: ``"completed"`` or ``"human_review_required"``.
        response: Customer-facing reply when the workflow completed.
        ticket_ref: Created ticket reference, if a ticket was created.
        interrupted: True when the workflow paused for human review.
        review_payload: Interrupt payload describing what needs review.
    """

    thread_id: str
    status: str
    response: str | None = None
    ticket_ref: str | None = None
    interrupted: bool = False
    review_payload: object | None = None


class HumanReviewRequest(BaseModel):
    """Reviewer decision used to resume an interrupted workflow.

    Attributes:
        decision: Reviewer decision (e.g. ``"approve_escalation"``).
        comments: Optional reviewer notes.
    """

    decision: str
    comments: str | None = None
