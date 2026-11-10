import sqlite3

from dataclasses import dataclass
from agents import function_tool, RunContextWrapper


MEMORY_DB = "longterm.db"


@dataclass
class UserContext:
    """Context containing authenticated user information."""

    user_id: str


def initialize_memory() -> None:
    """Initialize the long-term memory database."""

    with sqlite3.connect(MEMORY_DB) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                user_id TEXT NOT NULL,
                memory_key TEXT NOT NULL,
                memory_value TEXT NOT NULL,
                PRIMARY KEY (user_id, memory_key)
            );
            """
        )


@function_tool
def remember_fact(
    ctx: RunContextWrapper[UserContext],
    key: str,
    value: str,
) -> str:
    """Save or update an important fact about the user.

    Args:
        key: Descriptive key identifying the memory.
        value: Information to remember.

    Returns:
        Confirmation message.
    """
    user_id = ctx.context.user_id

    print(f"[Memory Write] {user_id}: {key} = {value}")

    with sqlite3.connect(MEMORY_DB) as connection:
        connection.execute(
            """
            INSERT INTO memories (user_id, memory_key, memory_value)
            VALUES (?, ?, ?)
            ON CONFLICT (user_id, memory_key)
            DO UPDATE SET memory_value = excluded.memory_value;
            """,
            (user_id, key, value),
        )

    return f"Successfully remembered {key}."


@function_tool
def recall_fact(
    ctx: RunContextWrapper[UserContext],
    key: str,
) -> str:
    """Retrieve a previously stored fact.

    Args:
        key: Memory key to retrieve.

    Returns:
        Stored memory value or a not-found message.
    """
    user_id = ctx.context.user_id

    with sqlite3.connect(MEMORY_DB) as connection:
        result = connection.execute(
            """
            SELECT memory_value
            FROM memories
            WHERE user_id = ? AND memory_key = ?;
            """,
            (user_id, key),
        ).fetchone()

    if result is None:
        return f"No memory found for '{key}'."

    print(f"[Memory Read] {user_id}: {key} = {result[0]}")

    return result[0]


@function_tool
def list_facts(
    ctx: RunContextWrapper[UserContext],
) -> str:
    """List all stored facts belonging to the current user.

    Returns:
        All stored memory keys and values.
    """
    user_id = ctx.context.user_id

    with sqlite3.connect(MEMORY_DB) as connection:
        results = connection.execute(
            """
            SELECT memory_key, memory_value
            FROM memories
            WHERE user_id = ?
            ORDER BY memory_key;
            """
        , (user_id,)).fetchall()

    if not results:
        return "No memories found for this user."

    print(f"[Memory List] {user_id}: {len(results)} memories")

    return "\n".join(
        f"{key}: {value}"
        for key, value in results
    )