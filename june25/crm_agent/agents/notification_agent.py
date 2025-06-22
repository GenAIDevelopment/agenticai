from langgraph.graph import StateGraph
from agents.utils import get_connection_string, get_llm, get_sql_database_toolkit
from langgraph.prebuilt import create_react_agent


connection_string = get_connection_string()
llm = get_llm()
sql_toolkit = get_sql_database_toolkit(llm=llm)

agent = create_react_agent(
    model=llm,
    tools=sql_toolkit.get_tools()
)
