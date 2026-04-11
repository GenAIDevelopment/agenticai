from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from typing import TypedDict, Literal
from typing_extensions import Annotated
# reducer
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import os

load_dotenv()
project = os.getenv('GOOGLE_CLOUD_PROJECT')


# model
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    vertexai = True,
    project = project
)



# lets create basic tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def subtract(a: int, b:int) -> int:
    """Subtract two numbers"""
    return a - b

@tool
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    return a / b

@tool
def get_weather(city: str) -> str:
    """Get the weather of the city"""
    return f"{city} is sunny"

# whole set of tools in an array
tools = [multiply, add, subtract, divide, get_weather]

# create a tool node
tool_node = ToolNode(tools=tools)

# create a model with bind tools
llm_with_tools = llm.bind_tools(tools=tools)

# define state
class AgentState(TypedDict):
    """State
    """
    messages: Annotated[list[BaseMessage], add_messages]
    answer: str

# This node invokes
def llm_node(state: AgentState):
    response = llm_with_tools.invoke(state['messages'])
    return {"messages": [response]}

def route_tools(state:AgentState) -> Literal["tools", "final"]:
    last_message = state['messages'][-1]

    if getattr(last_message, 'tool_calls', None):
        return "tools"
    
    return "final"

def final_result(state: AgentState):
    print(state["messages"][-1].pretty_print())
    state["answer"] = state["messages"][-1].content
    return state
# build the graph

graph = StateGraph(AgentState)
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)
graph.add_node("final_response", final_result)


graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    route_tools,
    {
        "tools": "tools",
        "final": "final_response"
    }
)
graph.add_edge("tools", "llm")
graph.set_finish_point("final_response")

if __name__ == "__main__":
    compile_graph = graph.compile()
    result = compile_graph.invoke({
        "messages": [
            HumanMessage(content="10 * 5")
        ]
    })

    for msg in result['messages']:
        print(f"{type(msg).__name__}  : {msg.content}")




