import os
from typing import Any

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
import json
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> MySQLConnection:
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USERNAME", "root"),
        password=os.getenv("MYSQL_PASSWORD", "rootpassword"),
        database=os.getenv("MYSQL_DATABASE", "library")
    )


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
    isbn: str
) -> None:

    with get_connection() as connection:

        with connection.cursor() as cursor:  # type: MySQLCursor

            query: str = """
            INSERT INTO books (
                id,
                title,
                author,
                published_year,
                available_copies,
                total_copies,
                genre,
                available,
                active,
                tags,
                isbn
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            book_data = (
                book_id,
                title,
                author,
                published_year,
                available_copies,
                total_copies,
                genre,
                available,
                active,
                json.dumps(tags),  # Convert Python list -> JSON string
                isbn
            )

            cursor.execute(query, book_data)

            connection.commit()

if __name__ == "__main__":
    add_book(
        "B008",
        "The Psychology of Money",
        "Morgan Housel",
        2020,
        5,
        5,
        "Finance",
        True,
        True,
        ["behavioral finance, investing, personal finance"],
        "9780062384802"
    )