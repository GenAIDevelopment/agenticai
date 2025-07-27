"""This module contains a single mcp server implementation
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp_template")


@mcp.tool()
def add(a: int, b: int) -> int:
    """This tool adds two number a, b

    Args:
        a (int): a
        b (int): b

    Returns:
        int: return a + b
    """
    return a + b
