from mcp.server.fastmcp import FastMCP, Context

from mcp.types import SamplingMessage, TextContent

mcp = FastMCP("Sampling Demo Server")


@mcp.tool()
async def explain(ctx: Context, topic:str) -> str:
    """
    Ask MCP Client to generate an explanation via MCP Sampling
    """
    prompt = f"Explain {topic} in simple terms"

    # This is key line: server -> client 
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                content=TextContent(
                    type="text",
                    text=prompt
                ),
                role="user"
            )
        ],
        system_prompt="You are a helpful teacher",
        max_tokens=400
    )
    return result.content.text


if __name__ == "__main__":
    mcp.run(transport="stdio")