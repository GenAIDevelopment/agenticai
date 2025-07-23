"""The main module of this project 
"""
import os
from dotenv import load_dotenv
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp_server.socialmedia.models import TextPostModel, ResponseState
from mcp_server.socialmedia.linkedin import create_text_post

mcp = FastMCP("SocialMedia")


@mcp.tool(name='post_to_linked_in')
def send_linked_in_post(post: TextPostModel) -> ResponseState:
    """This method creates a social media post to linkedin

    Args:
        post (TextPostModel): post details

    Returns:
        ResponseState: Suceess or Failure
    """
    return create_text_post(post.token, post.message)


if __name__ == "__main__":
    load_dotenv()
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    uvicorn.run(mcp.streamable_http_app, host=host, port=port)
