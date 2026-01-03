from typing import TypedDict, Annotated, Optional

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


# 1. State
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    approved: Optional[bool]
    review_notes: Optional[str]
# 2. Model
llm = ChatOllama(model="llama3.1:8b", temperature=0.2)


# 3. Node

def chat_node(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# add approval_gate

def approval_gate(state: AgentState) -> AgentState:
    last = state["messages"][-1].content
    decision = interrupt({
        "title": "Approve the assistant's draft?",
        "draft": last,
        "instructions": "Reply with approved=true/false with optional notes"
    })
    return {
        "approved": bool(decision["approved"]),
        "review_notes": decision["review_notes"]
    }

def finalize_node(state: AgentState) -> AgentState:
    if state["approved"]:
        return {}
    notes = state["review_notes"] or "No notes provided"
    revise_prompt = (
        "Revise your previous answer based on review notes"
        f"Review notes: {notes}"
    )
    response = llm.invoke(revise_prompt)
    return {
        "messages": [response],
        "approved": None,
        "review_notes": None
   }

# 4. Graph
builder = StateGraph(AgentState)
builder.add_node("chat", chat_node)
builder.add_node("approval", approval_gate)
builder.add_node("finalize", finalize_node)
builder.set_entry_point("chat")
builder.add_edge("chat", "approval")
builder.add_edge("approval", "finalize")
builder.set_finish_point("finalize")


checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)\


# 5. A simple cli runner that handles interrupt/resume
def run_once(user_text:str, thread_id:str = "demo-thread"):
    cfg = {"configurable": {"thread_id": thread_id}}
    for event in graph.stream(
        {"messages": [HumanMessage(content=user_text)]},
        config=cfg,
        stream_mode="updates"
    ):
        # When hitl is triggers Langgraph will emit an __interrupt__ event
        if "__interrupt__" in event:
            raw = event["__interrupt__"]
            print(raw)
            payload =raw[0].value
            print("Human in th loop Approval required")
            print(payload)
            ans = input("Approve? (y/n): ")
            notes = None
            if ans == "y":
                approved = True
            else:
                approved = False
                notes = input("Rejection Notes: ")
            resume_cmd = Command(
                resume={"approved": approved, "review_notes": notes}
            )
            final_state = graph.invoke(resume_cmd, cfg)

            print("Final state:")
            print(final_state["messages"][-1].content)
            return


if __name__ == "__main__":
    user_text = input("You: ")
    run_once(user_text)


