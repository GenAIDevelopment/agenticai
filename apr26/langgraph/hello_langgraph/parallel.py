from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from typing_extensions import Annotated
import operator


# reducer
def my_choice(existing, new):
    return new

class State(TypedDict):
    message: Annotated[list[str], operator.add]
    #message: Annotated[list[str], my_choice]
    student: str


def message_from_friend(state:State):
    return {"message": ["You will Win"]}

def message_from_enemy(state:State):
    return {"message": ["You will die trying but not win"]}


graph = StateGraph(State)
graph.add_node("friend", message_from_friend)
graph.add_node("enemy", message_from_enemy)

graph.add_edge(START, "friend")
graph.add_edge(START, "enemy")

graph.add_edge("friend", END)
graph.add_edge("enemy", END)

if __name__ == "__main__":
    compiled_graph = graph.compile()
    result = compiled_graph.invoke(
        State(student="Shyam")
    )
    print(result)