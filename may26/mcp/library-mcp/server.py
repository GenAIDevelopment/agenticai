from mcp.server.fastmcp import FastMCP
from datastore import BOOKS, STUDENTS
from datetime import date
from dotenv import load_dotenv
import db

load_dotenv()

mcp = FastMCP("library-mcp", host="0.0.0.0", port="19000")

@mcp.tool(name="search_books", description="Searches the active books by title, author or keyword. Optional filter by genre")
def search_books(query: str, genre: str="") -> list[dict]:
    """Searches the active books by title, author or keyword
    Optional filter by genre

    Args:
        query (str): Search keyword (title/author)
        genre (str): Optional genre

    Returns:
        list[dict]: list of books
    """
    q = query.lower()
    results = []
    for book in BOOKS.values():
        if not book["active"]:
            continue
        hit = q in book["title"].lower() or q in book["author"].lower()
        genre_ok = (genre == "") or ( genre.lower() in book["genre"].lower())
        if hit and genre_ok:
            results.append(book)
    return results or [{"message": "No books found"}]

@mcp.tool(name="add_book", description="Add a new book to the library")
def add_book(
    book_id: str,
    title: str,
    author: str,
    published_year: int,
    available_copies: int,
    total_copies: int,
    genre: str,
    available: bool,
    active: bool,
    tags: list[str],
    isbn: str ) -> str:
    """Add a new book to the library

    Args:
        book_id (str): Unique book id
        title (str): Book title
        author (str): Author name
        published_year (int): Year published
        available_copies (int): Number of copies available
        total_copies (int): Total number of copies
        genre (str): Book genre
        available (bool): Is the book available
        active (bool): Is the book active
        tags (list[str]): List of tags
        isbn (str): ISBN number
    """
    db.add_book(book_id, title, author, published_year, available_copies, total_copies, genre, available, active, tags, isbn)
    return f"Added book {title} to the library"
    

@mcp.resource("library://catalog")
def get_catalog() -> str:
    """
    Full books catalog
    """
    lines = ["---- College Library Catalog -----"]
    for book in BOOKS.values():
        status = "RETIRED" if not book['active'] else "AVAILABLE"
        lines.append(f"{book['id']}: {book['title']} by {book['author']} [{book['genre']}] - {status}")
    return "\n".join(lines)


@mcp.resource("library://students/{student_id}")
def get_student_profile(student_id:str) -> str:
    """
    Student profile
    """
    student = STUDENTS.get(student_id)
    if not student:
        return f"Student with id {student_id} not found"
    lines = ["---  Student Profile ---"]
    lines.append(f"Name: {student['name']}")
    lines.append(f"Email: {student['email']}")
    return "\n".join(lines)

@mcp.prompt(name="return_due_today", description="Return all books due today")
def return_due_today() -> str:
    """Return all books due today prompt
    """
    return (
        f"Today is {date.today()}. \n"
        "From LOANS, identify: \n"
        "  1. Due Today = due_date == today"
        "  2. Overdue = due_date < today \n"
        "  3. Due this week = due_date > today and due_date < today + 7 days \n"
        "Format the output as a prompt for the librarian."
    )

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
