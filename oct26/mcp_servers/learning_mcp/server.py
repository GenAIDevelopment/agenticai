from mcp.server import MCPServer

# mcp server object
mcp = MCPServer(
    "Calculator", 
    instructions="Simple Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): Number 1.
        b (int): Number 2.

    Returns:
        int: Sum of two numbers.
    """
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """Subtract the second number from the first number.

    Args:
        a (int): Number 1.
        b (int): Number 2.

    Returns:
        int: Difference between two numbers.
    """
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.

    Args:
        a (int): Number 1.
        b (int): Number 2.

    Returns:
        int: Product of two numbers.
    """
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide the first number by the second number.

    Args:
        a (int): Dividend.
        b (int): Divisor.

    Returns:
        float: Quotient of the division.

    Raises:
        ZeroDivisionError: If the divisor is zero.
    """
    return a / b

@mcp.tool()
def modulus(a: int, b: int) -> int:
    """Calculate the remainder after division.

    Args:
        a (int): Dividend.
        b (int): Divisor.

    Returns:
        int: Remainder after division.

    Raises:
        ZeroDivisionError: If the divisor is zero.
    """
    return a % b

@mcp.resource("calc://constants")
def constants() -> str:
    return (
        "pi = 3.14\n"
        "e = 2.718\n"
        "1 inch = 2.54 cm"
    )

@mcp.resource("calc://table/{number}")
def table(number: int) -> str:
    return "\n".join(f"{number} * {i} = {number * i}" for i in range(1, 11))


app = mcp.streamable_http_app()

if __name__ == "__main__":

    mcp.run("stdio")
    #mcp.run("streamable-http", host="0.0.0.0", port="8000")