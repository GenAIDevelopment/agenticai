from langgraph.graph import StateGraph
from langgraph.graph import START, END
import time


from typing import TypedDict, Annotated, Literal

class OperationsState(TypedDict, total=False):
    a: int
    b: int
    count: int
    result: int

def add(state: OperationsState) -> OperationsState:
    time.sleep(2)
    state['result'] = state['a'] + state['b']
    state['count'] += 1
    return state

def decision(state: OperationsState) -> Literal["pending", "completed"]:
    if state['count'] < 3:
        return "pending"
    return "completed"

graph_state = StateGraph(OperationsState)
graph_state.add_node("add", add)

graph_state.add_edge(START, "add")
graph_state.add_conditional_edges(
    "add", 
    decision,
    {
        "pending": "add",
        "completed": END
    }
)

graph = graph_state.compile()