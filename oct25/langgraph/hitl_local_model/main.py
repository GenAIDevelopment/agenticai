from typing import TypedDict, Annotated

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages


# 1. State
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 2. Model
llm = ChatOllama(model="llama3.1:8b", temperature=0.2)


# 3. Node

def chat_node(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 4. Graph
builder = StateGraph(AgentState)
builder.add_node("chat", chat_node)
builder.set_entry_point("chat")
builder.set_finish_point("chat")

graph = builder.compile()

if __name__ == "__main__":
    user_text = input("You: ")
    result = graph.invoke(
        {"messages": [HumanMessage(content=user_text)]}
    )
    print("\n Assistant: ", result["messages"][-1].content)
    
