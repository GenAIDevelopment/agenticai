"""Low-level database access for the customer care system.

This module owns the SQLAlchemy engine and a small set of helper functions
used by the write-side repository code. The language-model SQL agent reads
the database through ``utils.get_sql_database_tools`` instead; this module is
used only for controlled, parameterized reads and writes performed directly
by the application.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv()


def get_database_url() -> str:
    """Return the database connection URL from the environment.

    Returns:
        str: SQLAlchemy connection string read from ``DATABASE_URL``,
        falling back to the local docker-compose Postgres instance.
    """
    return os.getenv(
        "DATABASE_URL",
        "postgresql://ccuser:ccpassword@localhost:5432/customer_care",
    )


def get_engine() -> Engine:
    """Create and return a SQLAlchemy engine.

    Returns:
        Engine: Engine configured with ``pool_pre_ping`` so stale
        connections are detected before use.
    """
    return create_engine(get_database_url(), pool_pre_ping=True)


engine = get_engine()


def execute_one(query: str, params: dict | None = None):
    """Execute a query and return a single row.

    Args:
        query: SQL statement with named (``:name``) parameters.
        params: Mapping of parameter names to values.

    Returns:
        The first result row, or ``None`` if there are no rows.
    """
    with engine.begin() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchone()


def execute_all(query: str, params: dict | None = None):
    """Execute a query and return all rows.

    Args:
        query: SQL statement with named (``:name``) parameters.
        params: Mapping of parameter names to values.

    Returns:
        A list of result rows (possibly empty).
    """
    with engine.begin() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchall()


def execute_write(query: str, params: dict | None = None):
    """Execute a write statement and return its first row if available.

    Use with ``RETURNING`` to fetch generated keys. The surrounding
    ``engine.begin()`` block commits automatically on success.

    Args:
        query: SQL statement with named (``:name``) parameters.
        params: Mapping of parameter names to values.

    Returns:
        The first returned row, or ``None`` when the statement returns no
        rows.
    """
    with engine.begin() as conn:
        result = conn.execute(text(query), params or {})
        try:
            return result.fetchone()
        except Exception:
            return None


if __name__ == "__main__":
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successful!")
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to connect to database: {exc}")
