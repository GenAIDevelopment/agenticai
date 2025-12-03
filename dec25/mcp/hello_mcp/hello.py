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

if __name__ == "__main__":
    mcp.run(transport="stdio")
