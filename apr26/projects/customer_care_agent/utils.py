"""Utility functions for configuring LangChain components.

This module provides helper functions for creating and configuring:

* Google Gemini language models
* Database connections
* SQL database toolkit tools

The functions in this module are intended to be reused by agents and
application services that require access to the configured LLM and
database resources.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import BaseChatModel
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from dotenv import load_dotenv
from langchain.tools import BaseTool
import os

load_dotenv()


def get_llm() -> BaseChatModel:
    """Create and return the language model instance.

    The model configuration is loaded using the Google Cloud project
    specified in the ``GOOGLE_CLOUD_PROJECT`` environment variable.

    Returns:
        BaseChatModel: Configured Gemini language model instance that can
        be used by LangChain agents and chains.
    """
    project = os.getenv("GOOGLE_CLOUD_PROJECT")

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("MODEL_NAME","gemini-2.5-flash-lite"),
        vertexai=True,
        project=project,
    )

    return llm


def get_database() -> SQLDatabase:
    """Create and return a database connection wrapper.

    The database connection URL is read from the ``DATABASE_URL``
    environment variable. If the variable is not set, a default
    PostgreSQL connection string is used.

    Returns:
        SQLDatabase: LangChain SQLDatabase instance configured for the
        target database.
    """
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://ccuser:ccpassword@localhost:5432/customer_care",
    )

    db = SQLDatabase.from_uri(db_url)

    return db


def get_sql_database_tools() -> list[BaseTool]:
    """Create and return SQL database tools for an agent.

    This function initializes a SQLDatabaseToolkit using the configured
    language model and database connection, then retrieves the tools
    provided by the toolkit.

    Returns:
        list[BaseTool]: Collection of SQL-related tools that can be used
        by a LangChain agent to inspect schemas, execute queries, and
        interact with the database.
    """
    toolkit = SQLDatabaseToolkit(
        db=get_database(),
        llm=get_llm(),
    )

    tools = toolkit.get_tools()

    return tools