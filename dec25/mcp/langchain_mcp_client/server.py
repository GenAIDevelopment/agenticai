from mcp.server.fastmcp import FastMCP

# creating a server
mcp = FastMCP("hello-mcp")

# define tools
@mcp.tool()
def add(a:int|float, b:int|float) -> int|float:
    """This method adds two numbers

    Args:
        a (int | float): number 
        b (int | float): number

    Returns:
        int|float: a + b
    """
    return a + b

@mcp.tool()
def subtract(a:int|float, b:int|float) -> int|float:
    """This method subtracts two numbers

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        int|float: a - b
    """
    return a - b

@mcp.tool()
def multiply(a:int|float, b:int|float) -> int|float:
    """This method multiplies two numbers

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        int|float: a * b
    """
    return a * b

@mcp.tool()
def divide(a:int|float, b:int|float) -> int|float:
    """This method divides two numbers

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        int|float: a / b
    """
    return a / b

@mcp.tool()
def mod(a:int|float, b:int|float) -> int|float:
    """This method returns the remainder of a divided by b

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        int|float: a % b
    """
    return a % b

if __name__ == "__main__":
    mcp.run(transport="stdio")
