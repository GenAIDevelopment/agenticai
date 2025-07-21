"""This module will be a test server to explore api calling
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dummy-mcp")

@mcp.tool()
async def get_all_products():
    """This will send a get request and post back the information
    """
    