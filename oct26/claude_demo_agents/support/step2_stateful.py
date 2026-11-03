"""
Step 2: A stateful support agent

New concepts:
    short-term memory   the SDK session IS the conversation; resume=<session_id> continues it
    thread mapping      our code remembers which session belongs to which customer
    session store       the SDK also mirrors every transcript into SQLite, so a resume
                        still works on another machine or after the local files are gone
"""
import asyncio
import json
import sqlite3
from pathlib import Path
from typing import Annotated, Any

from claude_agent_sdk import query, tool, ToolAnnotations, ResultMessage
from dotenv import load_dotenv

from common import ORDERS, ok, fail, print_message, make_options
from session_store_sqlite import SqliteSessionStore

DATA_DIR = Path(__file__).parent / "downloads"     # fixed location, not "wherever you ran it from"
DATA_DIR.mkdir(exist_ok=True)                      # sqlite can't create a missing folder

SESSION_STORE = SqliteSessionStore(DATA_DIR / "sessions.db")   # ONE store for the whole process

RULES = """You are the customer support agent for QuickBite, a food delivery app.
- For order status, ETA or items, always call get_order_status. Never answer from memory.
"""


class Threads:
    """customer -> session_id. The SessionStore keeps transcripts; it doesn't know customers."""

    def __init__(self, path: Path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS threads (customer_id TEXT PRIMARY KEY, session_id TEXT NOT NULL)")

    def get(self, customer: str) -> str | None:
        row = self.db.execute("SELECT session_id FROM threads WHERE customer_id=?", (customer,)).fetchone()
        return row[0] if row else None

    def save(self, customer: str, session_id: str) -> None:
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO threads VALUES (?, ?)", (customer, session_id))

    def end(self, customer: str) -> None:
        with self.db:
            self.db.execute("DELETE FROM threads WHERE customer_id=?", (customer,))


THREADS = Threads(DATA_DIR / "threads.db")


def build_tools(customer: str) -> list:
    """Tools for ONE customer. The customer ID comes from here, never from the model."""

    @tool(
        "get_order_status",
        "Look up the live status of one of this customer's orders. Always use this for "
        "order status, ETA or items; never answer them from memory.",
        {"order_id": Annotated[str, "Order ID, e.g. 'QB-5521'"]},
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    async def get_order_status(args: dict[str, Any]) -> dict[str, Any]:
        order_id = args["order_id"].strip().upper()
        order = ORDERS.get(customer, {}).get(order_id)
        if not order:
            return fail(f"No order {order_id} for this customer. "
                        f"Their orders: {', '.join(ORDERS.get(customer, {})) or 'none'}.")
        return ok(json.dumps(order))

    return [get_order_status]


async def ask(customer: str, text: str) -> None:
    """Continue this customer's thread (or start one) and remember the session it used."""
    options = make_options(RULES, build_tools(customer),
                           resume=THREADS.get(customer),      # None the first time = new session
                           session_store=SESSION_STORE)
    try:
        async for message in query(prompt=text, options=options):
            print_message(message)
            if isinstance(message, ResultMessage):
                THREADS.save(customer, message.session_id)    # next question resumes this
    except Exception as error:
        print(f"  (run ended: {error})")


async def chat(customer: str, new_thread: bool = False) -> None:
    if new_thread:
        THREADS.end(customer)
    state = "Continuing" if THREADS.get(customer) else "Starting"
    print(f"{state} the thread for {customer}. Type 'quit' to stop.\n")
    while True:
        text = input("Customer: ").strip()
        if text.lower() in {"quit", "exit"}:                  # lower() - with the brackets
            break
        if text:
            await ask(customer, text)


if __name__ == "__main__":
    import sys
    load_dotenv()
    asyncio.run(chat("cust_101", new_thread="--new" in sys.argv))