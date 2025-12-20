import uuid

from typing import TypedDict, Literal, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict, total=False):
    to: str
    subject: str

    draft: str
    approval: Literal["approve", "reject"]
    feedback: str

    sent: bool



def draft_email(state: State):
    state["draft"] = f"""Subject: {state['subject']}

Hi Team,

We are rolling out a new feature and need your input. Please provide your feedback on the following:

{state['feedback']}

Best regards,
{state['to']}
"""
    return {"draft": state["draft"]}

def human_approval(state: State):
    decision = interrupt(
        {
            "type": "email_approval",
            "to": state["to"],
            "subject": state["subject"],
            "draft": state["draft"],
            "instructions": (
                "Approve or reject this email \n"
                "Resume with \n"
                "approved \n"
                "rejected"
            )
        }
    )
    if decision == 'approved':
        return {"approval": "approve"}
    return {
        "approval": "reject",
        "feedback": "Recompose"
        }

def send_email(state: State):

    state["sent"] = True
    return {"sent": True}


builder = StateGraph(State)
builder.add_node("draft_email", draft_email)
builder.add_node("human_approval", human_approval)
builder.add_node("send_email", send_email)

builder.add_edge(START, "draft_email")
builder.add_edge("draft_email", "human_approval")
builder.add_conditional_edges(
    "human_approval",
    lambda state: state["approval"],
    {
        "approve": "send_email",
        "reject": "draft_email",
    },
)
builder.add_edge("send_email", END)

graph = builder.compile(checkpointer=InMemorySaver())

# plumbing functions to start the graph, resume the graph and get the state of graph
def start_run(run_id: str, request_text: str):
    cfg = {
        "configurable": {"thread_id": run_id},
    }
    return graph.invoke({"request": request_text}, cfg)


def resume_run(run_id: str, decision: Dict[str, Any]):
    cfg= {
        "configurable": {"thread_id": run_id},
    }
    return graph.invoke(Command("resume", decision), config=cfg)


def get_state(run_id: str):
    cfg= {
        "configurable": {"thread_id": run_id},
    }
    return graph.get_state(cfg)
