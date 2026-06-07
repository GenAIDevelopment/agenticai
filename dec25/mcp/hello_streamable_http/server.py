from mcp.server.fastmcp import FastMCP
from typing import Union

from fastapi import FastAPI

app = FastAPI()

mcp = FastMCP("sse-demo")

@mcp.tool()
def add(a: int, b: int):
    """Adds two numbers"""
    return a + b

@mcp.tool()
def echo(message: str):
    """Echoes a string"""
    return f"you said {message}"

@app.get("/")
def read_root():
    return {"Hello": "World"}

# # lifecycle manager
# @asynccontextmanager
# async def combined_lifespan(app: FastAPI):
#     # Run both lifespans
#     async with app_lifespan(app):
#         async with mcp_app.lifespan(app):
#             yield



# mount
mcp_app = mcp.streamable_http_app()
app.mount("/mcp", mcp_app)

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")