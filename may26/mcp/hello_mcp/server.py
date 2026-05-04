from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="hello-mcp-python")

@mcp.tool(name="greet", description="Say hello to someone")
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool(name="scold", description="Curse someone")
def scold(name: str) -> str:
    return f"Hello, {name}! you are cursed"

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")

if __name__ == '__main__':
    main()