from mcp.server.fastmcp import FastMCP
from datastore import BOOKS


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


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
