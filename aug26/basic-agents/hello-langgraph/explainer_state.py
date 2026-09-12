from langgraph.graph import StateGraph
from langgraph.graph import START, END

from typing import TypedDict, Annotated
import operator
from operator import add as magic
import time

from langgraph.graph.message import MessagesState


class OperationsState(TypedDict, total=False):
    a: int
    b: int
    result: Annotated[list[int], magic ]


def add(state: OperationsState):
    return {
        "result": [state['a'] + state['b']]
    }

def sub(state: OperationsState):
    return {
            "result": [state['a'] - state['b']]
    }

def mul(state:OperationsState):
    return {
        "result": [state['a'] + state['b']]
    }


state_graph = StateGraph(OperationsState)

# defining nodes
state_graph.add_node("add", add)
state_graph.add_node("sub", sub)
#state_graph.add_node("mul", mul)

# define edges for direction

state_graph.add_edge(START, "add")
state_graph.add_edge(START, "sub")
#state_graph.add_edge(START, "mul")
#state_graph.add_edge("mul", END)
state_graph.add_edge("sub", END)
state_graph.add_edge("add", END)

# Compile the graph
graph = state_graph.compile()

if __name__ == "__main__":
    result = graph.invoke(OperationsState(a=10,b=5))
    print(result)



    

