from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Demo")

@mcp.tool()
def add(a:int, b: int) -> int:
    """Adds two numbers

    Args:
        a (int): a
        b (int): b

    Returns:
        int: a + b
    """
    return a + b

@mcp.tool()
def sub(a:int, b: int) -> int:
    """Subtracts two numbers

    Args:
        a (int): a
        b (int): b

    Returns:
        int: a - b
    """
    return a - b


if __name__ == "__main__":
    mcp.run(transport='stdio')
