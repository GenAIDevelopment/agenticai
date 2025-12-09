"""MCP server for Swiggy-like customer, order, and restaurant data retrieval.

This module sets up a FastMCP server exposing:
- Tools for fetching customer summaries, order details, and restaurant data.
- Resource endpoints for refund policies and complaint resolution documents.

All business logic is sample/demo logic and should be adapted for production.
"""

from mcp.server.fastmcp import FastMCP
from customers import CUSTOMERS
from orders import ORDERS
from restaurants import RESTARAUNTS

mcp = FastMCP(
    name="swiggy-mcp",
    website_url="https://github.com/shaikkhajaibrahim",
)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def get_customer_summary(customer_id: str) -> dict | None:
    """Retrieve customer summary details by customer ID.

    Args:
        customer_id (str): Unique identifier of the customer.

    Returns:
        dict | None: Customer profile data if found, otherwise ``None``.
    """
    for customer in CUSTOMERS:
        if customer['customerId'] == customer_id:
            return customer
    return None


@mcp.tool()
def get_order_information(order_id: str) -> dict | None:
    """Retrieve order information by order ID.

    Args:
        order_id (str): Unique identifier of the order.

    Returns:
        dict | None: Order details if found, otherwise ``None``.
    """
    for order in ORDERS:
        if order['orderId'] == order_id:
            return order
    return None


@mcp.tool()
def get_restaurant_information(restaurant_id: str) -> dict | None:
    """Retrieve restaurant information by restaurant ID.

    Args:
        restaurant_id (str): Unique identifier of the restaurant.

    Returns:
        dict | None: Restaurant details if found, otherwise ``None``.
    """
    for restaurant in RESTARAUNTS:
        if restaurant['restaurantId'] == restaurant_id:
            return restaurant
    return None


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

@mcp.resource("policy://refund")
def get_refund_policy() -> str:
    """Load and return the refund policy documentation.

    Returns:
        str: Contents of the `refundpolicy.md` file.
    """
    return read_markdown_file('refundpolicy.md')


@mcp.resource("complaint://{ctype}")
def get_complaint_resolution(ctype) -> str:
    """Return complaint resolution text for the given complaint type.

    Note:
        Currently this always loads from `latetimedelivery.md` regardless of
        the complaint type. Replace with proper logic as needed.

    Args:
        ctype (str): Complaint category.

    Returns:
        str: Complaint-resolution content.
    """
    return read_markdown_file('latetimedelivery.md')


def read_markdown_file(file_path):
    """
    Reads the content of a Markdown file with UTF-8 encoding.

    Args:
        file_path (str): The path to the Markdown file.

    Returns:
        str: The content of the Markdown file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
