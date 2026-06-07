from langgraph.graph import START, END, StateGraph
from typing import TypedDict

class Input(TypedDict):
    a: int
    b: int
    result: int|None


def perform_math(state: Input) -> Input:
    state['result'] = state['a'] + state['b']
    return state

state_graph = StateGraph(Input)
state_graph.add_node("add", perform_math)
state_graph.add_edge(START, "add")
state_graph.add_edge("add", END)

graph = state_graph.compile()