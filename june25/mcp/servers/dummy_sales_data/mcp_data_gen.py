"""This module will have mcp server to generate sales data
"""
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("data-generator")


@mcp.tool()
def create_user():
    pass


@mcp.tool()
def create_product():
    pass


@mcp.tool()
def create_category():
    pass


@mcp.resource(uri="products://latest")
def get_products():
    pass


@mcp.resource(uri="users://latest")
def get_users():
    pass


@mcp.resource(uri="categories://latest")
def get_categories():
    pass


if __name__ == '__main__':
    mcp.run(transport='stdio')
