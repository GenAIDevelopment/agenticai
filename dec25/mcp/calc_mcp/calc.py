from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="calc-mcp")

@mcp.tool()
def add(a: int|float, b: int|float) -> int|float:
    """Adds two numbers

    Args:
        a (int): number
        b (int): number

    Returns:
        int: a + b
    """
    return a + b

@mcp.tool()
def multiply(a: int|float, b: int|float) -> int|float:
    """Multiplies two numbers

    Args:
        a (int): number
        b (int): number

    Returns:
        int: a * b
    """
    return a * b

@mcp.tool()
def divide(a: int|float, b: int|float) -> float:
    """Divides two numbers

    Args:
        a (int): number
        b (int): number

    Returns:
        float: a / b
    """
    return a / b

@mcp.tool()
def subtract(a: int|float, b: int|float) -> int|float:
    """Subtracts two numbers

    Args:
        a (int): number
        b (int): number

    Returns:
        int: a - b
    """
    return a - b

@mcp.resource(uri="data://operations")
def operations() -> list[str]:
    return ["add", "sub", "mul", "div"]


@mcp.resource(uri="data://operation/{intent}")
def get_operation(intent:str) -> str:
    if intent == "add":
        return "add"
    else:
        return "idont know"



if __name__ == "__main__":
    mcp.run(transport="stdio")