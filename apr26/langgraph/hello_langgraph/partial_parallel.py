from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    fin_dept: bool = False
    lib_dept: bool = False
    sports_dept: bool = False
    student_id: str


def financial_department_check(state: State):
    return { "fin_dept": True }

def library_department_check(state: State):
    return { "lib_dept": True }

def sports_department_check(state: State):
    return { "sports_dept": True }

graph = StateGraph(State)
graph.add_node("fin", financial_department_check)
graph.add_node("lib", library_department_check)
graph.add_node("sports", sports_department_check)

graph.add_edge(START, "fin")
graph.add_edge(START, "lib")
graph.add_edge(START, "sports")

graph.add_edge("fin", END)
graph.add_edge("lib", END)
graph.add_edge("sports", END)

if __name__ == "__main__":
    compiled_graph = graph.compile()
    result = compiled_graph.invoke(State(student_id='i1001'))
    print(result)