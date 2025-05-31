from typing_extensions import TypedDict
from typing import Optional
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.graph import StateGraph, START, END

class QuestionState(TypedDict):
    messages: list[HumanMessage|AIMessage]
    question: str

model_id = "gemini-2.0-flash-lite-001"
llm = init_chat_model(model=model_id, model_provider="google_vertexai")

def ask_question(state: QuestionState) -> QuestionState:
    state['messages'] = [HumanMessage(state["question"])]
    response = llm.invoke(state['messages'])
    print(response.content)
    state["messages"].append(response)
    return state

graph_builder = StateGraph(QuestionState)
graph_builder.add_node("ask", ask_question)
graph_builder.add_edge(START, "ask")
graph_builder.add_edge("ask", END)

graph = graph_builder.compile()