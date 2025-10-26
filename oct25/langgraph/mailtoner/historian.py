from typing import TypedDict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph
import os


class HistoryState(TypedDict):
    date: str
    history: str


load_dotenv()
model_name = os.getenv('MODEL_NAME')
model_provider = os.getenv('MODEL_PROVIDER')
llm = init_chat_model(model=model_name, model_provider=model_provider)


def gather_history(state: HistoryState) -> HistoryState:
    date = state['date']
    prompt = ChatPromptTemplate([
        ('system', 'You are a historian good with dates'),
        ("user", "Given the  {date} "),
        ("user", "Find atleast 10 historic events which signify the date")
    ])

    chain = prompt | llm
    response = chain.invoke({'date': date})
    state['history'] = response.content
    return state


history_graph = StateGraph(HistoryState)

history_graph.add_node("history", gather_history)
history_graph.add_edge(START, "history")
history_graph.add_edge("history", END)

graph = history_graph.compile()
