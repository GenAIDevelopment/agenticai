from mcp.server.fastmcp import FastMCP
from datastore import BOOKS, STUDENTS
from datetime import date
from dotenv import load_dotenv
import db
from operations import issue_book

load_dotenv()

mcp = FastMCP("library-mcp", host="0.0.0.0", port="19000")

@mcp.tool(name="issue_book")
def issue_book(student_id, book_id, date) -> str:
    pass
    


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
