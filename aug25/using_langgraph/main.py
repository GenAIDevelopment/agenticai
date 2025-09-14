from langgraph.graph import StateGraph, END
from langchain.chat_models import init_chat_model

# Defined the state
class State(dict):
    input: str
    output: str

# Create a llm

llm = init_chat_model(
    "gemini-2.5-flash-lite",
    model_provider="google_vertexai"
)


def start_node(state: State) -> State:
    state["output"] = f"you said {state['input']}"
    return state

def llm_node(state: State) -> State:
    response = llm.invoke(state['input'])
    state["output"] = state['output'] + f"\n {response.content}"
    return state

# Build a graph
graph = StateGraph(State)
graph.add_node("start", start_node)
graph.add_node("llm", llm_node)

graph.set_entry_point("start")
graph.add_edge("start", "llm")
graph.add_edge("llm", END)



if __name__ == "__main__":
    # compile the graph
    app = graph.compile()
    result = app.invoke({"input": "What is capital of france"})
    print(result)

