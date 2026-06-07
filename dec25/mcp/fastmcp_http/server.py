from fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP("Streamable Demo")

@mcp.tool()
def add(a: int, b: int):
    """Adds two numbers"""
    return a + b

@mcp.tool()
def echo(message: str):
    """Echoes a string"""
    return f"you said {message}"


@mcp.tool()
async def some_long_running(a: int, b: int, ctx: Context) -> int:
    ctx.info("Starting long running task")
    asyncio.sleep(0.1)
    ctx.info("Finished long running task")
    # ctx progress
    ctx.report_progress(0.25, 1.0)
    ctx.report_progress(0.5, 1.0)
    ctx.report_progress(0.75,1.0)
    ctx.report_progress(1.0,1.0)
    return a * b

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)