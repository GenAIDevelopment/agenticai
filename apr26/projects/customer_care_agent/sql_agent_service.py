"""SQL agent for customer care database operations.

This module creates a LangChain SQL agent that can query the customer
care database and answer support-related questions.

The agent is configured with read-only guidance and is intended to
assist customer support workflows by finding products, similar tickets,
known resolutions, and suitable support agents.
"""

import utils
from langchain.agents import create_agent


def build_sql_agent():
    """Create and configure the customer care SQL agent.

    The agent is equipped with SQL database tools and a system prompt
    that restricts database interactions to read-only operations. It is
    designed to help support workflows by retrieving information from
    the customer care database.

    Returns:
        Any: Configured LangChain agent capable of answering questions
            about the customer care database.
    """
    tools = utils.get_sql_database_tools()
    llm = utils.get_llm()

    system_prompt = """
You are a customer care database assistant.

You can read the customer care database to help a support workflow,

Database Tables:
- products
- customers
- agents
- tickets
- resolutions
- comments

Database Views
- v_agent_performance
- v_ticket_overview
- v_resolution_summary

Your Job:
1. Find matching products
2. Find similar resolved tickets
3. Find known resolutions
4. Find suitable support agents
5. Summarize findings clearly

Important rules:
- Prefer Select queries only
- Do not INSERT, UPDATE, DELETE, DROP, ALTER OR TRUNCATE
- If you need to create or update ticket, say that the application should do it
- Limit results to at most 5 rows unless asked otherwise
- When searching for known resolutions, prefer resolved tickets joined
  with resolutions
- Return concise, structured answers
"""

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

def ask_database(question: str) -> str:
    """Execute a natural-language query against the database.

    A new SQL agent is created for the request, and the supplied
    question is processed using the agent and its SQL tools.

    Args:
        question: Natural-language question to ask about the customer
            care database.

    Returns:
        str: Agent-generated response based on database information.
    """
    agent = build_sql_agent()
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )
    return result


if __name__ == "__main__":
    question = "Give me the count of total tickets where status is in_progress"
    answer = ask_database(question)
    print(answer)
