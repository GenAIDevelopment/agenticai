"""Ticket management operations for the customer care system.

This module provides helper functions for creating support tickets and
retrieving related database information such as customers, products,
and support agents.

The functions in this module encapsulate database access logic used by
the customer care workflow when creating and assigning support tickets.
"""

from database import execute_one, execute_many, execute_write


def find_customer_id_by_email(email: str) -> int | None:
    """Find a customer identifier by email address.

    Args:
        email: Customer email address.

    Returns:
        int | None: Customer identifier if a matching customer exists;
        otherwise None.
    """
    if not email:
        return None

    row = execute_one(
        "SELECT id FROM customers WHERE email = :email",
        {"email": email},
    )

    return row["id"] if row else None


def find_product_id(
    product_hint: str | None,
    complaint_text: str,
) -> int | None:
    """Find a product identifier using a product hint.

    Args:
        product_hint: Product name or partial product name supplied by
            the customer.
        complaint_text: Customer complaint text. Included for future
            matching strategies.

    Returns:
        int | None: Product identifier if a matching product is found;
        otherwise None.
    """
    if not product_hint:
        return None

    row = execute_one(
        "SELECT id FROM products WHERE name ILIKE :product_hint",
        {"product_hint": f"%{product_hint}%"},
    )

    return row["id"] if row else None


def find_agent_id_for_category(
    category: str,
    priority: str,
) -> tuple[int | None, str | None]:
    """Find an appropriate support agent for a ticket.

    Agent selection is based on the ticket category and priority.

    Args:
        category: Classified ticket category.
        priority: Assigned ticket priority.

    Returns:
        tuple[int | None, str | None]: A tuple containing the selected
        agent identifier and agent email address. Returns
        ``(None, None)`` if no suitable agent is found.
    """
    if priority == "critical":
        department = "Escalations"
    elif category in (
        "product_defect",
        "warranty_claim",
        "software_issue",
    ):
        department = "Tier 2 Support"
    else:
        department = "Tier 1 Support"

    row = execute_one(
        """
        SELECT agent_id, email
        FROM agents
        WHERE department = :department
        ORDER BY agent_id
        LIMIT 1
        """,
        {"department": department},
    )

    if not row:
        return None, None

    return row["agent_id"], row["email"]


def get_next_ticket_ref() -> str:
    """Generate the next customer-facing ticket reference.

    Returns:
        str: Ticket reference in the format
        ``TKT-2026-00001``.
    """
    row = execute_one("SELECT COUNT(*) FROM tickets")

    next_number = row[0] + 1

    return f"TKT-2026-{next_number:05d}"


def create_ticket(
    customer_email: str | None,
    product_hint: str | None,
    complaint_text: str,
    channel: str,
    category: str,
    priority: str,
) -> dict:
    """Create a new support ticket and assign an agent.

    The function resolves customer, product, and agent information
    before creating a new support ticket in the database.

    Args:
        customer_email: Customer email address.
        product_hint: Product name or identifier provided by the
            customer.
        complaint_text: Customer complaint description.
        channel: Communication channel used by the customer.
        category: Classified issue category.
        priority: Assigned issue priority.

    Returns:
        dict: Ticket creation details containing:

            * ``ticket_id`` - Internal ticket identifier.
            * ``ticket_ref`` - Customer-facing ticket reference.
            * ``assigned_agent_email`` - Assigned support agent email.
    """
    customer_id = find_customer_id_by_email(customer_email)
    product_id = find_product_id(product_hint, complaint_text)

    ticket_ref = get_next_ticket_ref()

    agent_id, agent_email = find_agent_id_for_category(
        category,
        priority,
    )

    ticket_id = execute_write(
        """
        INSERT INTO tickets (
            ticket_ref,
            customer_id,
            product_id,
            subject,
            channel,
            category,
            priority,
            status
        ) VALUES (
            :ticket_ref,
            :customer_id,
            :product_id,
            :agent_id,
            :subject,
            :description,
            :channel,
            :category,
            :priority,
            'open'
        ) RETURNING ticket_id
        """,
        {
            "ticket_ref": ticket_ref,
            "customer_id": customer_id,
            "product_id": product_id,
            "agent_id": agent_id,
            "subject": complaint_text,
            "description": complaint_text,
            "channel": channel,
            "category": category,
            "priority": priority,
        },
    )

    return {
        "ticket_id": ticket_id,
        "ticket_ref": ticket_ref,
        "assigned_agent_email": agent_email,
    }