from typing_extensions import TypedDict
from typing import Optional
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

class QuestionState(TypedDict):
    question: str
    response: Optional[str]

model_id = "gemini-2.0-flash-lite-001"
llm = init_chat_model(model=model_id, model_provider="google_vertexai")


def ask_llm(state: QuestionState) -> QuestionState:
    message = HumanMessage(state["question"])
    response = llm.invoke([message])
    state['response']= response.content
    return state

graph_builder = StateGraph(QuestionState)
graph_builder.add_node("brain", ask_llm)
graph_builder.add_edge(START,"brain")
graph_builder.add_edge("brain", END)

graph = graph_builder.compile()

