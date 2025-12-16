from fastmcp import FastMCP

mcp = FastMCP("Streamable Demo")

@mcp.tool()
def add(a: int, b: int):
    """Adds two numbers"""
    return a + b

@mcp.tool()
def echo(message: str):
    """Echoes a string"""
    return f"you said {message}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)