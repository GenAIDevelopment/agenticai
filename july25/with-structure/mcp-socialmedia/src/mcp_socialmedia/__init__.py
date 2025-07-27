"""
This is entrypoint
"""
import os
import uvicorn
from dotenv import load_dotenv
from mcp_socialmedia.server import mcp


def main() -> None:
    """Entry point for the package
    """
    load_dotenv()
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    uvicorn.run(mcp.streamable_http_app, host=host, port=port)
