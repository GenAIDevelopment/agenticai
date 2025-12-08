from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="swiggy-mcp",
    website_url="https://github.com/shaikkhajaibrahim",
    )


## tools

@mcp.tool()
def get_customer_summary(customer_id:str):
    pass

@mcp.tool
def get_order_information(order_id:str):
    pass

@mcp.tool
def get_restaurant_information(restaurant_id:str):
    pass


## resources
@mcp.resource("policy://refund")
def get_refund_policy() -> str:
    lines = []
    with open('refundpolicy.md') as refund:
        lines = refund.readlines()
    return "\n".join(lines)

@mcp.resource("complaint://{ctype}")
def get_complaint_resolution(ctype) -> str:
    lines = []
    with open('latetimedelivery.md') as refund:
        lines = refund.readlines()
    return "\n".join(lines)