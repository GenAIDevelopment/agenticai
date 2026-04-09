from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from typing_extensions import Annotated


class State(TypedDict):
    query: str
    response: str

# where we make decision
def process_question(state:State) -> Literal["finance", "sports", "admin"]:
    if 'fee' in state['query']:
        return "finance"
    elif 'sport' in state['query'] or 'game' in state['query']:
        return "sports"
    else:
        return "admin"

def fin_response(state: State):
    return {"response": "Pay your fee"}

def admin_dept(state: State):
    return {"response": "Meet me tommorow"}

def sports_dept(state: State):
    return {"resonse": "Physical Trainer is on leave"}

graph = StateGraph(State)

graph.add_node("fin", fin_response)
graph.add_node("adm", admin_dept)
graph.add_node("sport", sports_dept)

graph.add_conditional_edges(
    START,
    process_question, # decision
    {
        "finance" : "fin",
        "sports": "sport",
        "admin": "adm"
    }

)
graph.add_edge("fin", END)
graph.add_edge("adm", END)
graph.add_edge("sport", END)

if __name__ == "__main__":
    compiled_graph = graph.compile()
    query = input("Enter your question")
    response = compiled_graph.invoke({
        "query": query
    })
    print(response)

