from mcp.server.fastmcp import FastMCP

mcp = FastMCP("math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Performs addition of  a, b

    Args:
        a (int): a value
        b (int): b value

    Returns:
        int: a + b
    """
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """Performs subtraction of a, b

    Args:
        a (int): a value
        b (int): b value

    Returns:
        int: a - b
    """
    return a - b

@mcp.tool()
def mul(a: int, b: int) -> int:
    """Performs multiplication of a, b

    Args:
        a (int): a value
        b (int): b value

    Returns:
        int: a * b
    """
    return a * b


@mcp.tool()
def div(a: int, b: int) -> int:
    """Performs division of a, b

    Args:
        a (int): a value
        b (int): b value

    Returns:
        int: a // b
    """
    return a // b


if __name__ == "__main__":
    mcp.run(transport='stdio')