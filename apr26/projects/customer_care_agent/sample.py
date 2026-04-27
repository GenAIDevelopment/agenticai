import os
from typing import Annotated

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from dotenv import load_dotenv


# ── 1. Connect to your Postgres container ────────────────────────────────────
DB_URL = "postgresql://ccuser:ccpassword@localhost:5432/customer_care"
db = SQLDatabase.from_uri(DB_URL)

# ── 2. LLM ───────────────────────────────────────────────────────────────────
load_dotenv()
project = os.getenv('GOOGLE_CLOUD_PROJECT')


# model
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    vertexai = True,
    project = project
)

# ── 3. Build the SQL toolkit and bind tools to the LLM ───────────────────────
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools   = toolkit.get_tools()           # list_tables, get_schema, query_sql, query_checker
llm_with_tools = llm.bind_tools(tools)


# ── 4. LangGraph state ───────────────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ── 5. Agent node: calls the LLM (with tools bound) ──────────────────────────
SYSTEM_PROMPT = """You are an expert SQL agent for a customer-care database.
Always look at the available tables first, inspect the relevant schema,
then write and execute a correct SQL query.
Return a clear, concise answer in plain English."""

def call_agent(state: AgentState) -> AgentState:
    from langchain_core.messages import SystemMessage
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# ── 6. Build the graph ───────────────────────────────────────────────────────
graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent",  call_agent)
graph_builder.add_node("tools",  ToolNode(tools))   # executes any tool calls

graph_builder.add_edge(START, "agent")

# If the LLM returned tool calls → run them, then loop back to agent.
# If not → we're done.
graph_builder.add_conditional_edges(
    "agent",
    tools_condition,            # built-in: checks for tool_calls in last message
)
graph_builder.add_edge("tools", "agent")

agent = graph_builder.compile()


# ── 7. Helper to run a natural-language query ─────────────────────────────────
def ask(question: str) -> str:
    from langchain_core.messages import HumanMessage
    result = agent.invoke({"messages": [HumanMessage(content=question)]})
    return result["messages"][-1].content


# ── 8. Example queries ────────────────────────────────────────────────────────
if __name__ == "__main__":
    questions = [
        "How many open or in-progress support tickets are there?",
        "Which product has the most complaints?",
        "What is the average customer rating for resolved tickets?",
        "List all critical tickets and who they are assigned to.",
        "Which agent has resolved the most tickets?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {ask(q)}")