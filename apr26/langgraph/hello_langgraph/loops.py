from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from typing_extensions import Annotated
import time


class State(TypedDict):
    application: str
    comments: list[str] = []
    retry_count: int = -1
    approved: bool

def apply(state: State):
    time.sleep(1)
    state["comments"] = ['A: Application looks okay']
    state['retry_count']  = state["retry_count"] + 1
    return state

def process(state: State):
    time.sleep(1)
    state['comments'] = ['B: Application looks okay']
    return state
    
def approval(state: State):
    time.sleep(1)
    state['comments'] = ['C: Approved']
    return state

def check_process(state:State) -> Literal["reapply", "next"]:
    time.sleep(2)
    if state["retry_count"] >= 2:
        return "next"
    return "reapply"


graph = StateGraph(State)
graph.add_node("A", apply)
graph.add_node("B", process)
graph.add_node("C", approval)

graph.add_edge(START, "A")
graph.add_edge("A", "B")
#graph.add_edge("B", "C")
graph.add_conditional_edges(
    "B",
    check_process,
    {
        "reapply": "A",
        "next": "C"

    }
)
graph.add_edge("C", END)

if __name__== "__main__":
    compiled_graph = graph.compile()
    application = input("Enter your application ")
    response = compiled_graph.invoke(
        State(
            application=application,
            comments=[],
            retry_count=-1,
            approved=False
        )
    )
    print(response)