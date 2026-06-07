"""Safe, deterministic write-side repository for support tickets.

The LLM is never allowed to insert tickets directly. Instead, the workflow
calls these parameterized functions, which resolve the customer, product, and
agent before creating a ticket. Column names match the schema in
``customercaredb/init.sql`` (``customer_id``, ``product_id``, ``agent_id``).
"""

from database import execute_all, execute_one, execute_write


def find_customer_id_by_email(email: str | None) -> int | None:
    """Look up a customer id by email address.

    Args:
        email: Customer email address, or ``None``.

    Returns:
        int | None: Matching ``customer_id``, or ``None`` if not found.
    """
    if not email:
        return None

    row = execute_one(
        """
        SELECT customer_id
        FROM customers
        WHERE email = :email
        """,
        {"email": email},
    )

    return row[0] if row else None


def find_product_id(product_hint: str | None, complaint_text: str) -> int | None:
    """Find a product id from a hint and the complaint text.

    First tries a direct ``LIKE`` match on name/brand/model; if that fails,
    falls back to scanning the product catalog for any token contained in the
    combined search text.

    Args:
        product_hint: Optional product name or partial name from the customer.
        complaint_text: Full complaint text, used as additional match context.

    Returns:
        int | None: Matching ``product_id``, or ``None`` if no product matches.
    """
    search_text = f"{product_hint or ''} {complaint_text}".lower()

    row = execute_one(
        """
        SELECT product_id, name, brand, model_number
        FROM products
        WHERE LOWER(name) LIKE :q
           OR LOWER(brand) LIKE :q
           OR LOWER(model_number) LIKE :q
        LIMIT 1
        """,
        {"q": f"%{(product_hint or '').lower()}%"},
    )

    if row:
        return row[0]

    # Fallback: scan products and match any catalog token in the search text.
    products = execute_all(
        """
        SELECT product_id, name, brand, model_number
        FROM products
        """
    )

    for product_id, name, brand, model_number in products:
        for candidate in (name, brand, model_number):
            if candidate and candidate.lower() in search_text:
                return product_id

    return None


def find_agent_id_for_category(
    category: str,
    priority: str,
) -> tuple[int | None, str | None]:
    """Select a support agent based on category and priority.

    Critical tickets route to Escalations; technical categories route to
    Tier 2 Support; everything else routes to Tier 1 Support.

    Args:
        category: Classified ticket category.
        priority: Assigned ticket priority.

    Returns:
        tuple[int | None, str | None]: ``(agent_id, agent_email)`` for the
        chosen agent, or ``(None, None)`` if no agent is found.
    """
    if priority == "critical":
        department = "Escalations"
    elif category in ("product_defect", "warranty_claim", "software_issue"):
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

    return row[0], row[1]


def get_next_ticket_ref() -> str:
    """Generate the next customer-facing ticket reference.

    Returns:
        str: Ticket reference in the form ``TKT-2026-00001``.
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
    """Create a support ticket and assign an agent.

    Args:
        customer_email: Customer email address.
        product_hint: Optional product name or hint.
        complaint_text: Customer complaint description.
        channel: Communication channel (chat, email, ...).
        category: Classified ticket category.
        priority: Assigned ticket priority.

    Returns:
        dict: ``{"ticket_id", "ticket_ref", "assigned_agent_email"}``.
    """
    customer_id = find_customer_id_by_email(customer_email)
    product_id = find_product_id(product_hint, complaint_text)
    agent_id, agent_email = find_agent_id_for_category(category, priority)
    ticket_ref = get_next_ticket_ref()

    subject = complaint_text[:120]

    row = execute_write(
        """
        INSERT INTO tickets (
            ticket_ref,
            customer_id,
            product_id,
            agent_id,
            channel,
            category,
            priority,
            status,
            subject,
            description
        )
        VALUES (
            :ticket_ref,
            :customer_id,
            :product_id,
            :agent_id,
            :channel,
            :category,
            :priority,
            'open',
            :subject,
            :description
        )
        RETURNING ticket_id
        """,
        {
            "ticket_ref": ticket_ref,
            "customer_id": customer_id,
            "product_id": product_id,
            "agent_id": agent_id,
            "channel": channel,
            "category": category,
            "priority": priority,
            "subject": subject,
            "description": complaint_text,
        },
    )

    return {
        "ticket_id": row[0],
        "ticket_ref": ticket_ref,
        "assigned_agent_email": agent_email,
    }
