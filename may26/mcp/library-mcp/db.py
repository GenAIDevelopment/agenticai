import os
from typing import Any

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
import json
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> MySQLConnection:
    """Create and return a new MySQL database connection using environment variables."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USERNAME", "root"),
        password=os.getenv("MYSQL_PASSWORD", "rootpassword"),
        database=os.getenv("MYSQL_DATABASE", "library")
    )


def execute_query(query: str, params: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    """
    Execute a SQL query with optional parameters.

    For SELECT queries, returns a list of result rows.
    For INSERT/UPDATE/DELETE queries, commits the transaction and returns an empty list.
    """
    with get_connection() as connection:

        with connection.cursor() as cursor:  # type: MySQLCursor

            cursor.execute(query, params)

            if cursor.description:
                return cursor.fetchall()

            connection.commit()
            return []


if __name__ == "__main__":
    result = execute_query('select * from authors')
    print(result)

    result = execute_query('select * from authors where author_id = %s', (1,))
    print(result)

    query = "INSERT INTO users (user_code, user_type, first_name, last_name, email, phone, password_hash, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = ('STU004', 'STUDENT', 'Alex', 'Mercer', 'alex.m1@student.edu', '555-0203',
              'studenthash4', 'ACTIVE', '2026-05-19 03:32:17', '2026-05-19 03:32:17')
    result = execute_query(query, params)
    print(result)
