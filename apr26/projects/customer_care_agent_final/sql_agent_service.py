"""Read-side database intelligence layer backed by an LLM SQL agent.

This service builds a LangChain agent over the ``SQLDatabaseToolkit`` tools so
the workflow can ask natural-language questions such as "is there a known
resolution for this complaint?". The agent is restricted to read-only
(SELECT) access; ticket creation and other writes are handled by the
deterministic repository code in :mod:`ticket_repository`.

The language model and SQL tools come from :mod:`utils`, which is configured
to use Google Generative AI (Gemini on Vertex AI).
"""

from langchain.agents import create_agent

from utils import get_llm, get_sql_database_tools

SYSTEM_PROMPT = """
You are a customer care database assistant.

You can read the customer care database to help a support workflow.

Database domain:
- Electronics products
- Customers
- Agents
- Support tickets
- Ticket resolutions
- Ticket comments
- Reporting views

Your job:
1. Find matching products.
2. Find similar resolved tickets.
3. Find known resolutions.
4. Find suitable support agents.
5. Summarize findings clearly.

Important rules:
- Prefer SELECT queries only.
- Do not INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
- If you need to create or update a ticket, say that the application should do it.
- Limit results to at most 5 rows unless asked otherwise.
- When searching for known resolutions, prefer resolved tickets joined with resolutions.
- Return concise, structured answers.
"""


def build_sql_agent():
    """Build the read-only SQL agent.

    Returns:
        A compiled LangChain agent configured with the Gemini model from
        :func:`utils.get_llm` and the SQL toolkit tools from
        :func:`utils.get_sql_database_tools`.
    """
    return create_agent(
        model=get_llm(),
        tools=get_sql_database_tools(),
        system_prompt=SYSTEM_PROMPT,
    )


# The agent is built lazily on first use. Building it opens a database
# connection (the toolkit inspects the schema), so we avoid doing that at
# import time — that keeps app startup and tests independent of a live DB.
_sql_agent = None


def get_sql_agent():
    """Return the singleton SQL agent, building it on first use."""
    global _sql_agent
    if _sql_agent is None:
        _sql_agent = build_sql_agent()
    return _sql_agent


def _content_to_text(content) -> str:
    """Normalize a chat message ``content`` value to plain text.

    Gemini (and other chat models) may return ``content`` either as a plain
    string or as a list of content blocks (strings or ``{"type": "text",
    "text": ...}`` dicts). This flattens any of those shapes into a string.

    Args:
        content: The ``content`` attribute of a chat message.

    Returns:
        str: The combined text content.
    """
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(block.get("text", ""))
        return "".join(parts)

    return str(content)


def ask_database(question: str) -> str:
    """Ask the SQL agent a natural-language question about the database.

    Args:
        question: Natural-language question for the agent to answer using
            read-only database tools.

    Returns:
        str: The agent's final textual answer.
    """
    result = get_sql_agent().invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    return _content_to_text(result["messages"][-1].content)
