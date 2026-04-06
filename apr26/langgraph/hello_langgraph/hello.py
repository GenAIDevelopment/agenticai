"""Hello langgraph 
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# lets create state
class MyState(TypedDict):
    """This class represents the state of the graph
    """
    name: str
    friends: list[str]
    family: list[str]

# node 1
def find_friends(state: MyState) -> MyState:
    """This function finds friends
    """
    state['friends'] = ['Ram', 'Shyam']
    return state

# node 2
def find_family(state: MyState) -> MyState:
    """This function finds family
    """
    state['family'] = ['sita', 'gita']
    return state

# graph which takes state as argument
graph = StateGraph(MyState)

graph.add_node("friends", find_friends)
graph.add_node("family", find_family)
graph.add_edge(START, "friends")
graph.add_edge("friends", "family")
graph.add_edge("family", END)

# compile the graph
compiled_graph = graph.compile()


if __name__ == "__main__":
    print(type(compiled_graph))
    response = compiled_graph.invoke({
        "name": "abc"
    })
    print(response)