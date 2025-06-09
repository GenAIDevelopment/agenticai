from langchain_core.messages import AnyMessage, HumanMessage
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph


def previous_n_messages(
        left: list[AnyMessage], 
        right: list[AnyMessage],
       ) -> list[AnyMessage]:
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]

    all = left + right
    return all[-3:]


class MyMessageState(TypedDict):
    messages: Annotated[ list[AnyMessage], previous_n_messages]


def node_1(state: MyMessageState)-> MyMessageState:
    state['messages'] = HumanMessage('I,m node 1')
    return state

def node_2(state: MyMessageState)-> MyMessageState:
    state['messages'] = HumanMessage('I,m node 2')
    return state

def node_3(state: MyMessageState)-> MyMessageState:
    state['messages'] = HumanMessage('I,m node 3')
    return state


my_graph_builder = StateGraph(MyMessageState)
my_graph_builder.add_node("1", node_1)
my_graph_builder.add_node("2", node_2)
my_graph_builder.add_node("3", node_3)
my_graph_builder.set_entry_point("1")
my_graph_builder.add_edge("1", "2")
my_graph_builder.add_edge("2", "3")
my_graph_builder.set_finish_point("3")
my_graph = my_graph_builder.compile()
