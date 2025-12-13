from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sse-demo")

@mcp.tool()
def add(a: int, b: int):
    """Adds two numbers"""
    return a + b

@mcp.tool()
def echo(message: str):
    """Echoes a string"""
    return f"you said {message}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")