from fastmcp import FastMCP, Context
from fastapi import FastAPI
import uvicorn
import asyncio

mcp = FastMCP()


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b


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


# create the http_app which is asgi
mcp_app = mcp.http_app(path="/")

# initialize fastap with mcp app lifespan
app = FastAPI(lifespan=mcp_app.lifespan)

# mount asgi app on an endpoint
app.mount("/mcp", mcp_app)


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


if __name__ == "__main__":

    # staring fastapi
    uvicorn.run(app, host="0.0.0.0", port=8000)
