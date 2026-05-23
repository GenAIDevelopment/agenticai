"""
Library MCP server.

This module is *only* the MCP surface: every tool / resource / prompt is a thin
wrapper that delegates to a function in `operations.py`, where all the SQL lives.
No database access happens directly here. Results are serialised to JSON text so
any MCP client can consume them (Decimal -> float, datetime -> ISO string).
"""

import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

import operations as ops

load_dotenv()

mcp = FastMCP("library-mcp", host="0.0.0.0", port="19000")


def _to_text(result: Any) -> str:
    """Serialise any operations result to readable JSON text for MCP clients."""

    def default(value: Any) -> Any:
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return str(value)

    return json.dumps(result, default=default, indent=2, ensure_ascii=False)


# ===========================================================================
# Tools — actions we want the AI to perform
# ===========================================================================
@mcp.tool()
def issue_book(student_id: str, book_id: int, date: str) -> str:
    """Issue an available copy of a book to a student (date = YYYY-MM-DD)."""
    return ops.issue_book(student_id, book_id, date)


@mcp.tool()
def process_return(student_id: str, book_id: int, date: str,
                   description: str = "") -> str:
    """Return a book; assesses a late fine if overdue. Returns the fine amount."""
    fine = ops.process_return(student_id, book_id, date, description)
    return _to_text({"fine_assessed": fine})


@mcp.tool()
def add_book(title: str, isbn13: str | None = None, subject: str | None = None,
             copies: int = 1) -> str:
    """Add a new title to the catalog with one or more copies."""
    book_id = ops.add_book(title, isbn13=isbn13, subject=subject, copies=copies)
    return _to_text({"book_id": book_id})


@mcp.tool()
def retire_book(book_id: int) -> str:
    """Withdraw a book and its available copies from circulation."""
    return ops.retire_book(book_id)


@mcp.tool()
def collect_fine(student_id: str, amount: float, method: str = "CASH") -> str:
    """Collect a payment and apply it to the student's oldest fines first."""
    applied = ops.collect_fine(student_id, amount, method=method)
    return _to_text({"amount_applied": applied})


@mcp.tool()
def issue_no_due_certificate(student_id: str) -> str:
    """Issue a no-dues certificate if the student has no fines and no open loans."""
    return _to_text(ops.issue_no_due_certificate(student_id))


@mcp.tool()
def create_account_statement(from_date: str, to_date: str) -> str:
    """Library financial statement between two dates (YYYY-MM-DD)."""
    return _to_text(ops.create_account_statement(from_date, to_date))


@mcp.tool()
def reserve_book(student_id: str, book_id: int) -> str:
    """Add a student to the reservation queue for a book."""
    reservation_id = ops.reserve_book(student_id, book_id)
    return _to_text({"reservation_id": reservation_id})


@mcp.tool()
def cancel_reservation(reservation_id: int) -> str:
    """Cancel an existing reservation."""
    return ops.cancel_reservation(reservation_id)


@mcp.tool()
def hold_book(book_id: int) -> str:
    """Physically set aside an available copy for pickup."""
    return ops.hold_book(book_id)


@mcp.tool()
def notify_student_about_reservation(student_id: str, book_id: int,
                                     reason: str = "Your reserved book is ready") -> str:
    """Mark a reservation READY and notify the student."""
    return _to_text(ops.notify_student_about_reservation(student_id, book_id, reason))


@mcp.tool()
def notify(student_id: str, message: str, channel: str = "SYSTEM",
           subject: str | None = None) -> str:
    """Send (log) a notification to a student."""
    notification_id = ops.notify(student_id, message, channel=channel, subject=subject)
    return _to_text({"notification_id": notification_id})


@mcp.tool()
def send_return_reminders(date: str | None = None) -> str:
    """Notify every borrower whose book is due today."""
    return _to_text({"notifications_sent": ops.send_return_reminders(date)})


@mcp.tool()
def deactivate_student(student_id: str, status: str = "INACTIVE") -> str:
    """Deactivate a student account (INACTIVE / BLOCKED / LEFT)."""
    return ops.deactivate_student(student_id, status)


@mcp.tool()
def process_damage(student_id: str, book_id: int, description: str,
                   damage_type: str = "OTHER", estimated_cost: float = 0.0) -> str:
    """File a damage report for a book and assess the repair cost as a fine."""
    return _to_text(ops.process_damage(student_id, book_id, description,
                                       damage_type, estimated_cost))


@mcp.tool()
def process_lost_book(student_id: str, book_id: int,
                      replacement_cost: float) -> str:
    """Mark a loaned book lost and charge the replacement cost."""
    return _to_text(ops.process_lost_book(student_id, book_id, replacement_cost))


@mcp.tool()
def update_policy(policy_id: str, new_policy: str) -> str:
    """Update a library policy value (policy_id may be id or key)."""
    return ops.update_policy(policy_id, new_policy)


@mcp.tool()
def add_subscription(journal_id: int, start_date: str, end_date: str,
                     cost: float = 0.0, access_type: str = "BOTH") -> str:
    """Create an article/journal subscription contract."""
    sub_id = ops.add_subscription(journal_id, start_date, end_date, cost, access_type)
    return _to_text({"subscription_id": sub_id})


@mcp.tool()
def update_book_rack(book_id: int, call_number: str | None = None,
                     shelf_location: str | None = None) -> str:
    """Update a book's shelf/rack location (rack management)."""
    return ops.update_book_rack(book_id, call_number, shelf_location)


# ===========================================================================
# Resources — data the AI can read
# ===========================================================================
@mcp.resource("book://{book_id}")
def book_info(book_id: int) -> str:
    """Full detail for a single book."""
    return _to_text(ops.book_info_by_id(int(book_id)))


@mcp.resource("book-id://{title}")
def book_id_by_title(title: str) -> str:
    """Resolve a (partial) title to matching book ids."""
    return _to_text(ops.get_book_id(title))


@mcp.resource("availability://{book_id}")
def availability(book_id: int) -> str:
    """Available vs total copies of a book."""
    return _to_text(ops.get_availability_by_id(int(book_id)))


@mcp.resource("rack://{book_id}")
def rack(book_id: int) -> str:
    """Shelf / rack location and call number for a book."""
    return _to_text(ops.get_book_rack(int(book_id)))


@mcp.resource("reservations://{book_id}")
def reservations_for_book(book_id: int) -> str:
    """Active reservation queue for a book."""
    return _to_text(ops.get_reservation_details_for_book(int(book_id)))


@mcp.resource("fine-due://{student_id}")
def fine_due(student_id: str) -> str:
    """Outstanding fine balance for a student."""
    return _to_text({"student_id": student_id, "fine_due": ops.get_fine_due(student_id)})


@mcp.resource("balance://{student_id}")
def account_balance(student_id: str) -> str:
    """Current account balance for a student."""
    return _to_text({
        "student_id": student_id,
        "current_balance": ops.total_account_balance(student_id),
    })


@mcp.resource("catalog://all")
def catalog() -> str:
    """Browse the active book catalog."""
    return _to_text(ops.get_book_catalog())


@mcp.resource("search://{query}")
def search(query: str) -> str:
    """Search the catalog by title, subject, ISBN or author."""
    return _to_text(ops.search_book(query))


@mcp.resource("subscriptions://active")
def active_subscriptions() -> str:
    """List currently active journal subscriptions."""
    return _to_text(ops.get_active_subscriptions())


# ===========================================================================
# Prompts — reusable prompt templates backed by live data
# ===========================================================================
@mcp.prompt()
def returns_due_today() -> str:
    """Draft reminder messages for books due back today."""
    due = ops.get_returns_due_today()
    return (
        "Here are the loans due back today:\n"
        f"{_to_text(due)}\n\n"
        "Draft a short, friendly return reminder for each borrower."
    )


@mcp.prompt()
def monthly_fine_collection_summary() -> str:
    """Summarise fine collection by month."""
    data = ops.monthly_fine_collection()
    return (
        "Monthly fine collection figures:\n"
        f"{_to_text(data)}\n\n"
        "Summarise the trend and call out the strongest and weakest months."
    )


@mcp.prompt()
def monthly_book_ledger_summary() -> str:
    """Summarise the book ledger by month and entry type."""
    data = ops.monthly_book_ledger()
    return (
        "Monthly book ledger movements:\n"
        f"{_to_text(data)}\n\n"
        "Summarise issues, returns and other activity per month."
    )


@mcp.prompt()
def top_performing_books() -> str:
    """Report the most-issued books."""
    data = ops.top_performing_books()
    return (
        "Top performing books by issue count:\n"
        f"{_to_text(data)}\n\n"
        "Write a short report on the most popular titles."
    )


@mcp.prompt()
def under_performing_books() -> str:
    """Report the least-issued books that could be retired."""
    data = ops.under_performing_books()
    return (
        "Under-performing books (below average issues):\n"
        f"{_to_text(data)}\n\n"
        "Recommend which titles to promote or consider retiring."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
