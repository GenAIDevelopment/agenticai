from langgraph.graph import StateGraph
from langgraph.graph import START, END
import time


from typing import TypedDict, Annotated, Literal

class OperationsState(TypedDict, total=False):
    a: int
    b: int
    operation: Literal["Add", "Sub"]
    result: int


def decision(state: OperationsState) -> Literal["add", "sub"]:
    time.sleep(2)
    if state["operation"] == "Add":
        return "add"
    return "sub"

def add(state: OperationsState):
    time.sleep(2)
    return {
        "result": state['a'] + state['b']
    }

def sub(state: OperationsState):
    time.sleep(2)
    return {
            "result": state['a'] - state['b']
    }

graph_state = StateGraph(OperationsState)

graph_state.add_node("add_node", add)
graph_state.add_node("sub_node", sub)

graph_state.add_conditional_edges(
    START,
    decision,
    {
        "add": "add_node",
        "sub": "sub_node"
    }
)

graph_state.add_edge("add_node", END)
#graph_state.set_finish_point("add_node")
graph_state.add_edge("sub_node", END)
#graph_state.set_finish_point("sub_node")

graph = graph_state.compile()


if __name__ == "__main__":
    result = graph.invoke(OperationsState(a=10,b=5, operation="Add"))
    print(result)
