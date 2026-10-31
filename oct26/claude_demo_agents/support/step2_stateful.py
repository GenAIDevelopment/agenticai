"""
Step 1: A stateless support agent

New Concepts:
    working memory   the context window of ONE run 
    live data
"""
from claude_agent_sdk import query, tool, ToolAnnotations
from typing import Annotated, Any
import asyncio
import json
from dotenv import load_dotenv
from common import ORDERS, ok, fail, print_message, make_options
from session_store_sqlite import SqliteSessionStore

RULES = """You are the customer support agent for QuickBite, a food delivery app.
- For order status, ETA or items, always call get_order_status. Never answer from memory
"""


def build_tools(customer: str) -> list:
    """Tools for ONE customer. The customer ID comes from here, never from model """

    @tool(
        "get_order_status",
        "Look up the live status of one of this customers order. Always use this for"
        "order status, ETA or items; never answer this from memory",
        {"order_id": Annotated[str, "Order Id, e.g. 'QB-5521'"]},
        annotations=ToolAnnotations(readOnlyHint=True)
    )
    async def get_order_status(args: dict[str, Any]) -> dict[str, Any]:
        order = ORDERS.get(customer, {}).get(args['order_id'].strip().upper())
        if not order:
            return fail(f"No order {args['order_id'].strip().upper()} for this customer {customer}")
        return ok(json.dumps(order))

    return [get_order_status]


async def ask_once(customer: str, text: str):
    """
    A brand new session for every question
    """
    try:
        async for message in query(
                prompt=text,
                options=make_options(
                    RULES, 
                    build_tools(customer), 
                    session_store=SqliteSessionStore(path="./downloads/sessions.db")
                )
            ):
            print_message(message)

    except Exception as error:
        print(f"  (run ended: {error})")


async def chat(customer: str) -> None:
    """A brand-new session for every question"""
    print(
        f"stateless chat for {customer}. Every qustion starts from nothing, Type quit to stop\n")
    while True:
        text = input("Customer:  ").strip()
        if text.lower in {"quit", "exit"}:
            break
        if text:
            await ask_once(customer, text)

# async def self_test() -> None:
#     tools = {t.name for t in build_tools("cust_101")}
#     print("live data: looked up never stored")
#     await

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(chat(customer="cust_101"))
