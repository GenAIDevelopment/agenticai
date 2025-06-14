from langgraph.graph import StateGraph
from typing import TypedDict
from typing import TypedDict
class MyState(TypedDict):
    message: str

from time import sleep
def node_1(state: MyState) -> MyState:
    state['message'] = "Im in node 1"
    sleep(2)
    return state

def node_2(state: MyState) -> MyState:
    state['message'] = "Im in node 2"
    sleep(2)
    return state

def node_3(state: MyState) -> MyState:
    state['message'] = "Im in node 3"
    sleep(2)
    return state

def node_4(state: MyState) -> MyState:
    state['message'] = "Im in node 4"
    sleep(2)
    return state

def node_5(state: MyState) -> MyState:
    state['message'] = "Im in node 5"
    sleep(2)
    return state

my_graph_builder = StateGraph(MyState)
my_graph_builder.add_node("node1", node_1)
my_graph_builder.add_node("node2", node_2)
my_graph_builder.add_node("node3", node_3)
my_graph_builder.add_node("node4", node_4)
my_graph_builder.add_node("node5", node_5)
my_graph_builder.set_entry_point("node1")
my_graph_builder.set_finish_point("node5")
my_graph_builder.add_edge("node1", "node2")
my_graph_builder.add_edge("node2", "node3")
my_graph_builder.add_edge("node3", "node4")
my_graph_builder.add_edge("node4", "node5")
my_graph = my_graph_builder.compile()
