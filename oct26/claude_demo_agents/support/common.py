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

def fail(text:str) -> dict[str, Any]:
    """A failed tool result"""
    return {"content": [{"type": "text", "text": text}], "is_error": True}

def ok(text:str) -> dict[str, Any]:
    """A successful tool result"""
    return {"content": [{"type": "text", "text": text}]}