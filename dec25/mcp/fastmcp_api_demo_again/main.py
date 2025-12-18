from fastmcp import FastMCP, Context
from fastapi import FastAPI
import uvicorn

mcp = FastMCP()


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b


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
