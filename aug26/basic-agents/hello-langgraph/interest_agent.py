from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Required
# Lets define state using typed dict

class InterestState(TypedDict, total=False):
    """This represents the state
    """
    principal: Required[float|int]
    time: Required[float|int]
    rate: Required[float|int]
    simple_interest: float
    compund_interest: float


def simple_interest(state: InterestState) -> InterestState:
    state['simple_interest'] = (state['principal'] * state['rate'] * state['time']) / 100
    return state

def compound_interest(state: InterestState) -> InterestState:
    amount = state['principal'] * ((1 + (state['rate'] / 100)) ** state['time'])
    
    # Subtract principal to get just the interest
    state['compund_interest'] = amount - state['principal']
    return state


state_graph = StateGraph(InterestState)
state_graph.add_node("si", simple_interest)
state_graph.add_node("ci", compound_interest)

state_graph.add_edge(START, "si")
state_graph.add_edge("si", "ci")
state_graph.add_edge("ci", END)

graph = state_graph.compile()

def collect_input(name, description) -> str:
    value = input(f"Enter {name} < {description} >")
    return value

if __name__ == "__main__":
    principal = float(collect_input("principal", "total amount"))
    time = float(collect_input("time", "total time in years"))
    rate = float(collect_input("rate", "annual rate of intrest"))
    state = InterestState(principal=principal, time=time, rate=rate)
    result = graph.invoke(state)
    print(result)