from __future__ import annotations

from typing import TypedDict, Annotated, Optional, Any, Dict, Union
from datetime import datetime, timezone
import hashlib
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, BaseMessage
from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


# ---------------------------
# Helpers (audit)
# ---------------------------
def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def audit_event(event_type: str, **kwargs) -> dict[str, Any]:
    return {"type": event_type, "ts": now_utc(), **kwargs}


# ---------------------------
# State
# ---------------------------
class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    approved: Optional[bool]
    review_notes: Optional[str]
    audit: list[dict[str, Any]]


# ---------------------------
# Model
# ---------------------------
llm = ChatOllama(model="llama3.1:8b", temperature=0.2)


# ---------------------------
# Nodes
# ---------------------------
def chat_node(state: AgentState) -> AgentState:
    """Generate the initial draft."""
    response = llm.invoke(state["messages"])
    draft = response.content

    audit = state.get("audit", [])
    audit = audit + [audit_event("draft_created", draft_hash=sha256_text(draft))]

    return {"messages": [response], "approved": None, "review_notes": None, "audit": audit}


def revise_node(state: AgentState) -> AgentState:
    """If rejected, revise the draft using review notes."""
    notes = state.get("review_notes") or "No notes given."
    audit = state.get("audit", [])

    revise_prompt = (
        "Revise your previous answer based on the reviewer's feedback.\n"
        f"Reviewer notes: {notes}"
    )

    response = llm.invoke(state["messages"] + [HumanMessage(content=revise_prompt)])
    revised = response.content

    audit = audit + [
        audit_event(
            "draft_revised",
            revised_hash=sha256_text(revised),
            reason_notes=notes,
        )
    ]

    return {"messages": [response], "approved": None, "review_notes": None, "audit": audit}


def approval_gate(state: AgentState):
    """
    HITL node:
    - interrupts to request human input
    - after resume, logs decision and routes using Command(goto=...)
    """
    draft = state["messages"][-1].content
    audit = state.get("audit", [])

    # Log: approval requested
    audit = audit + [audit_event("approval_requested", draft_hash=sha256_text(draft))]

    decision = interrupt(
        {
            "title": "Approve the assistant's draft?",
            "draft": draft,
            "instructions": "Send approved=true/false with optional notes.",
        }
    )

    approved = bool(decision.get("approved", False))
    notes = decision.get("notes")
    reviewer = decision.get("reviewer_id", "unknown")

    # Log: decision
    audit = audit + [
        audit_event(
            "approval_decision",
            approved=approved,
            reviewer_id=reviewer,
            notes=notes,
            draft_hash=sha256_text(draft),
        )
    ]

    if approved:
        return Command(update={"approved": True, "review_notes": notes, "audit": audit}, goto=END)

    return Command(update={"approved": False, "review_notes": notes, "audit": audit}, goto="revise")


# ---------------------------
# Build graph
# ---------------------------
builder = StateGraph(AgentState)
builder.add_node("chat", chat_node)
builder.add_node("approve", approval_gate)
builder.add_node("revise", revise_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", "approve")
builder.add_edge("revise", "approve")

# IMPORTANT: checkpointer is what makes HITL resume possible
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)


# ---------------------------
# API models
# ---------------------------
class StartRequest(BaseModel):
    user_text: str = Field(..., min_length=1)
    thread_id: Optional[str] = None  # allow caller to provide one


class ResumeRequest(BaseModel):
    approved: bool
    notes: Optional[str] = None
    reviewer_id: str = "unknown"


class NeedsApprovalResponse(BaseModel):
    status: str = "needs_approval"
    thread_id: str
    payload: Dict[str, Any]


class CompletedResponse(BaseModel):
    status: str = "completed"
    thread_id: str
    output: str
    audit: list[dict[str, Any]] = []


RunResponse = Union[NeedsApprovalResponse, CompletedResponse]


# ---------------------------
# Core runner: "run until interrupt or end"
# ---------------------------
def run_until_interrupt_or_end(
    stream_input: Union[dict, Command],
    thread_id: str,
) -> RunResponse:
    config = {"configurable": {"thread_id": thread_id}}

    for event in graph.stream(stream_input, config=config, stream_mode="updates"):
        if "__interrupt__" in event:
            interrupt_obj = event["__interrupt__"][0]
            payload = getattr(interrupt_obj, "value", None)

            # payload should be dict from our interrupt(...) call
            if not isinstance(payload, dict):
                payload = {"message": str(payload)}

            return NeedsApprovalResponse(thread_id=thread_id, payload=payload)

    # No interrupt => finished (or at least reached a stable point)
    state = graph.get_state(config).values
    output = state["messages"][-1].content if state.get("messages") else ""
    audit = state.get("audit", [])
    return CompletedResponse(thread_id=thread_id, output=output, audit=audit)


# ---------------------------
# FastAPI
# ---------------------------
app = FastAPI(title="LangGraph HITL API (Ollama)")


@app.post("/runs", response_model=RunResponse)
def start_run(req: StartRequest):
    thread_id = req.thread_id or uuid.uuid4().hex
    return run_until_interrupt_or_end(
        stream_input={"messages": [HumanMessage(content=req.user_text)]},
        thread_id=thread_id,
    )


@app.post("/runs/{thread_id}/resume", response_model=RunResponse)
def resume_run(thread_id: str, req: ResumeRequest):
    # If thread_id is unknown (no checkpoint), get_state will typically fail later.
    # We'll do a lightweight existence check:
    try:
        _ = graph.get_state({"configurable": {"thread_id": thread_id}})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Unknown thread_id or missing checkpoint: {e}")

    cmd = Command(
        resume={
            "approved": req.approved,
            "notes": req.notes,
            "reviewer_id": req.reviewer_id,
        }
    )
    return run_until_interrupt_or_end(stream_input=cmd, thread_id=thread_id)


@app.get("/runs/{thread_id}")
def get_run_state(thread_id: str):
    """Optional debugging endpoint to inspect state."""
    config = {"configurable": {"thread_id": thread_id}}
    try:
        values = graph.get_state(config).values
        # Keep response small
        return {
            "thread_id": thread_id,
            "approved": values.get("approved"),
            "review_notes": values.get("review_notes"),
            "last_message": values["messages"][-1].content if values.get("messages") else None,
            "audit": values.get("audit", []),
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
