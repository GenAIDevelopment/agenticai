from langchain.tools import tool
from langchain.messages import AIMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from utils import get_default_model
import time


@tool
def get_weather(city: str) -> str:
    """Get the current weather forecast for a specified city.

    Args:
        city: The name of the city (e.g., 'London', 'Tokyo').

    Returns:
        A string describing the current weather conditions.
    """
    time.sleep(1)
    return f"Weather in {city} is sunny today"

@tool
def get_capital(country: str) -> str:
    """Retrieve the capital city of a given country.

    Args:
        country: The full name of the country (e.g., 'France', 'Japan').

    Returns:
        A string stating the capital city of the country.
    """
    time.sleep(1)
    return f"The capital of {country} is Paris"

@tool
def get_currency(country: str) -> str:
    """Get the official currency used in a specific country.

    Args:
        country: The full name of the country (e.g., 'Germany', 'Brazil').

    Returns:
        A string specifying the official currency of the country.
    """
    time.sleep(1)
    return f"The currency of {country} is Euros"

tools = [get_weather, get_capital, get_currency]

# llm
llm = get_default_model()

# llm aware of tools
llm_with_tools = llm.bind_tools(tools=tools)


def chat(state: MessagesState) -> MessagesState:
    time.sleep(1)
    state['messages'] = llm_with_tools.invoke(state["messages"])
    time.sleep(1)
    return state
tool_node = ToolNode(tools=tools)

graph_state = StateGraph(MessagesState)

graph_state.add_node("chat", chat)
graph_state.add_node("tools", tool_node)

graph_state.set_entry_point("chat")
graph_state.add_conditional_edges(
    "chat",
    tools_condition
)
graph_state.add_edge("tools", "chat")
graph_state.add_edge("chat", END)

graph = graph_state.compile()

if __name__ == "__main__":
    graph.invoke({
        "messages": [
            HumanMessage("What is capital of France & how is weather there"),
        ]
    })



