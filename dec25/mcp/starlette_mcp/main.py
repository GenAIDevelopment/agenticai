from starlette.applications import Starlette
from starlette.routing import Mount, Host
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

app = Starlette(routes=[
    Mount("/", app=mcp.sse_app())
])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
