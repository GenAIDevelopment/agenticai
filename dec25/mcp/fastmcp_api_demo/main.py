from fastmcp import FastMCP, Context
from fastapi import FastAPI
import time

mcp = FastMCP("FastMCP API Demo")
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

@mcp.tool()
def dummy_long_lived_task(a:int, b: int, ctx:Context):
    ctx.info("Starting long lived task")
    ctx.report_progress(0.1)
    time.sleep(5)
    ctx.report_progress(0.5)
    time.sleep(5)
    ctx.report_progress(0.9)
    ctx.info("Finished long lived task")
    return a + b

app.mount("/mcp", mcp.http_app(transport="streamable-http"))


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    # start fast api


