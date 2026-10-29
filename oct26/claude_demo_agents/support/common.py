"""
common.py - common utils class
"""

from typing import Any, Callable

from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server,
    AssistantMessage, ResultMessage, TextBlock, ToolUseBlock,
)

ORDERS = {
    "cust_101": {"QB-5521": {"status": "out for delivery", "eta": "8:40 pm", "items": "2 * veg biryani"}},
    "cust_202": {"QB-7710": {"status": "delivered", "eta": None, "items": "1 * Haleem"}}
}

ENV = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}


def fail(text: str) -> dict[str, Any]:
    """A failed tool result"""
    return {"content": [{"type": "text", "text": text}], "is_error": True}


def ok(text: str) -> dict[str, Any]:
    """A successful tool result"""
    return {"content": [{"type": "text", "text": text}]}


def make_options(
        system_prompt: str,
        tools: list,
        resume: str | None = None,
        max_turns: int = 6) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        system_prompt=system_prompt,
        resume=resume,
        mcp_servers={"support": create_sdk_mcp_server(
            name="support",
            version="1.0.0",
            tools=tools
        )},
        tools=[],
        allowed_tools=["mcp__support__*"],
        permission_mode="dontAsk",
        setting_sources=[],
        env=ENV,
        max_turns=max_turns
    )


def print_message(message) -> None:
    """
    Show tool calls and replies as they stream in
    """
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                print(f"   [tool] {block.name.split('__')[-1]} {block.input}")
            elif isinstance(block, TextBlock):
                print(f"Agent: {block.text}")


async def chat_loop(
        options: ClaudeAgentOptions,
        on_result: Callable[[ResultMessage], None] | None = None) -> None:
    """
    One live conversation: every message joins the same session
    """
    async with ClaudeSDKClient(options=options) as client:
        while True:
            text = input("Customer: ").strip()
            if text.lower() in {"quit", "exit"}:
                break
            if not text:
                continue
            await client.query(text)
            async for message in client.receive_response():
                print_message(message)
                if isinstance(message, ResultMessage) and on_result:
                    on_result(message)


async def run_thread(
    store,
    customer: str,
    new_thread: bool,
    system_prompt: str,
    tools: list
) -> str | None:
    """
    Open or continue this customers thread, chat and return its session id
    """
    if new_thread:
        store.end_thread(customer)
    session_id = store.get_thread(customer)
    print(f"{'Continuing' if session_id else 'New'} thread for {customer}. Type 'quit' to stop \n")
    options = make_options(
        system_prompt,
        tools,
        resume=session_id
    )
    await chat_loop(
        options,
        on_result=lambda m: store.save_thread(customer, m.session_id)
    )
    return store.get_thread(customer)
