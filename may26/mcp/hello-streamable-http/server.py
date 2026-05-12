from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="streamable-mcp-demo",
    host="localhost",
    port=18000,
)

@mcp.tool(name="add")
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool(name="subtract")
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
