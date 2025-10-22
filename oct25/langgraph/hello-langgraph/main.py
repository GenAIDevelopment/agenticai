from langgraph.graph import START, END, StateGraph
from typing import TypedDict


class MyState(TypedDict):
    name: str
    message: str


def say_hello(state: MyState) -> MyState:
    """This is wish node

    Every node in langraph takes state as input and returns 
    state

    Args:
        state (MyState): State

    Returns:
        MyState: State
    """
    print(state)
    state['message'] = f"hello {state['name']}"
    return state

# design your graph
state_graph = StateGraph(MyState)
state_graph.add_node("wish", say_hello)
state_graph.add_edge(START, "wish")
state_graph.add_edge("wish", END)

# compile your graph
graph = state_graph.compile()
