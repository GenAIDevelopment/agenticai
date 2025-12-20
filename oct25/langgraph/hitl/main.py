import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email_hitl import start_run, resume_run, get_state
from email import send_email

app = FastAPI(title="Email HITL")

class StartRequest(BaseModel):
    request: str
    approver_email: str


class DecisionRequest(BaseModel):
    decision: str
    email_drafter: str | None = None


@app.post("/runs")
def create_run(payload: StartRequest):
    run_id = str(uuid.uuid4())
    # this will stop executing on interrupt
    start_run(run_id, payload.request)

    st = get_state(run_id)
    draft = st.values["draft"]
    # send email with approve_reject links as content
    content = f"""
    <p>{draft}</p>
    <p>Approve: /runs/{run_id}/decision </p>
    <p>Reject: /runs/{run_id}/decision </p>
    """
    send_email(payload.approver_email, payload.approver_email, "Email HITL", content )
    return {"run_id": run_id, "status": "PENDING_APPROVAL"}


@app.get("/runs/{run_id}")
def get_run_status(run_id: str):
    st = get_state(run_id)
    if st.is_finished():
        return {"run_id": run_id, "status": "COMPLETED"}
    return {"run_id": run_id, "status": "PENDING_APPROVAL"}


@app.post("/runs/{run_id}/decision")
def approve_or_reject(
    run_id: str, 
    payload: DecisionRequest):
    if payload.decision in ["approve", "reject"]:
        out = resume_run(run_id, {"approval": payload.decision})
        st = get_state(run_id)
        return {
            "run_id": run_id, 
            "status": "COMPLETED",
            "decision": payload.decision,
            "result": out,
            "sent": st.values["sent"]
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid decision")

    