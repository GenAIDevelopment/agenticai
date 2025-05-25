from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal, Optional

class CalcState(TypedDict):
    """State
    """
    number1: float
    number2: float
    operator: Literal["+", "-"]
    result: Optional[float]

def add(state: CalcState) -> CalcState:
    """add node
    """
    state['result'] = state['number1'] + state['number2']
    return state

def sub(state: CalcState) -> CalcState:
    """subtract node
    """
    state['result'] = state['number1'] - state['number2']
    return state

def my_router(state: CalcState) -> Literal["add", "sub"]:
    if state['operator'] == '+':
        return "add"
    else:
        return "sub"


graph_builder = StateGraph(CalcState)
graph_builder.add_node("add", add)
graph_builder.add_node("sub", sub)

graph_builder.add_conditional_edges(START,my_router)
graph_builder.add_edge("sub",END)
graph_builder.add_edge("add",END)

graph = graph_builder.compile()
