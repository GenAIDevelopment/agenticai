from fastmcp import Client
import asyncio


async def main():
    async with Client("http://localhost:19000/mcp") as client:
        # get tools
        tools = await client.list_tools()
        print(tools)

        # use a tool add_book to
        result = await client.call_tool(
            "add_book",
            {
                "book_id": "B017",
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "published_year": 2008,
                "available_copies": 4,
                "total_copies": 6,
                "genre": "Software Engineering",
                "available": True,
                "active": True,
                "tags": ["clean-code", "programming", "best-practices"],
                "isbn": "9780132350883"
            }
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
