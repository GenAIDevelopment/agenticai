from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain.tools import tool
from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
gemini_llm = init_chat_model(
    model="gemini-2.0-flash-lite-001", model_provider="google_vertexai")
# Tools are where we have our functionality and we want llm to call our tool


@tool("addition", parse_docstring=True, return_direct=True)
def add(a: int, b: int) -> int:
    """Addition of two numbers

    Args:
      a : number
      b : number

    Returns: sum of a, b
    """
    return a + b


@tool("subtraction", parse_docstring=True, return_direct=True)
def sub(a: int, b: int) -> int:
    """Subtract two numbers

    Args:
      a : number
      b : number

    """
    return a - b


@tool("multipy", parse_docstring=True, return_direct=True)
def mul(a: int, b: int) -> int:
    """Multiplication of two numbers

    Args:
      a : number
      b : number

    """
    return a * b


@tool("divide", parse_docstring=True, return_direct=True)
def div(a: int, b: int) -> int:
    """division of two numbers

    Args:
      a : number
      b : number

    """
    return a // b


load_dotenv()

tool_node = ToolNode([add, sub, mul, div])
prompt = SystemMessage(
    "You are an arthimetic expert who uses tools, if tools are not identified try generating response on your own")
agent = create_react_agent(
    model=gemini_llm,
    tools=tool_node,
    prompt=prompt)

# stategraph = StateGraph(MessagesState)

# stategraph.add_node("agent", agent)
# stategraph.add_edge(START, "agent")
# stategraph.add_edge("agent", END)

# graph = stategraph.compile()
graph = agent