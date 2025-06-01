from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langgraph.prebuilt import ToolNode

load_dotenv()
gemini_llm = init_chat_model(model="gemini-2.0-flash-lite-001", model_provider="google_vertexai")


@tool("divide", parse_docstring=True, return_direct=True)
def div(a: int, b: int) -> int:
    """division of two numbers

    Args:
      a : number
      b : number

    """
    return a // b

@tool("multipy", parse_docstring=True, return_direct=True)
def mul(a: int, b: int) -> int:
    """Multiplication of two numbers

    Args:
      a : number
      b : number

    """
    return a * b

@tool("subtraction", parse_docstring=True, return_direct=True)
def sub(a: int, b: int) -> int:
    """Subtract two numbers

    Args:
      a : number
      b : number

    """
    return a - b

@tool("addition", parse_docstring=True, return_direct=True)
def add(a: int, b: int) -> int:
    """Addition of two numbers

    Args:
      a : number
      b : number

    """
    return a + b

# open weather map
weather = OpenWeatherMapAPIWrapper()
weather_tool = weather.run

# Tavily_tool

tavily_tool = TavilySearch(
    max_results=3,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)

tools = [add, sub, mul, div, weather_tool, tavily_tool ]

tool_node = ToolNode(tools)
gemini_llm_with_tools = gemini_llm.bind_tools(tools)

def call_model(state: MessagesState) -> MessagesState:
    """This is llm node
    """
    state['messages'] = gemini_llm_with_tools.invoke(state['messages'])
    return state

tools_graph_builder:StateGraph = StateGraph(MessagesState)
tools_graph_builder.add_node("llm", call_model)
tools_graph_builder.add_node("tools", tool_node)
tools_graph_builder.add_edge("llm", "tools")
tools_graph_builder.set_entry_point("llm")
tools_graph_builder.set_finish_point("tools")

graph = tools_graph_builder.compile()