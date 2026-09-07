from langgraph.graph import StateGraph
from langgraph.graph import START, END

from typing import TypedDict
import time


class OperationsState(TypedDict):
    a: int
    b: int
    sum: None|int
    product: None|int
    diff: None|int


def add(state: OperationsState) -> OperationsState:
    time.sleep(2)
    state['sum'] = state['a'] + state['b']
    return state

def sub(state: OperationsState) -> OperationsState:
    time.sleep(2)
    state['diff'] = state['a'] - state['b']
    return state

def mul(state:OperationsState) -> OperationsState:
    time.sleep(2)
    state['product'] = state['a'] * state ['b']
    return state


state_graph = StateGraph(OperationsState)

# defining nodes
state_graph.add_node("add", add)
state_graph.add_node("sub", sub)
state_graph.add_node("mul", mul)

# define edges for direction

state_graph.add_edge(START, "add")
state_graph.add_edge("add", "sub")
state_graph.add_edge("sub", "mul")
state_graph.add_edge("mul", END)

# Compile the graph
graph = state_graph.compile()

if __name__ == "__main__":
    result = graph.invoke(OperationsState(a=5,b=4))
    print(result)



    

