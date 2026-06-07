# Customer Care Agent (MVP)

A practical customer-care workflow built with **LangGraph + LangChain
SQLDatabaseToolkit + FastAPI + PostgreSQL + uv**, using **Google Gemini
(Vertex AI)** as the language model.

---

## Purpose

This project demonstrates a **safe, production-shaped agentic workflow** for
electronics customer support. When a customer submits a complaint, the system:

1. **Understands** the complaint and detects the product.
2. **Searches the support database** (past tickets + resolutions) using an LLM
   SQL agent to see if it's a *known issue with a known fix*.
3. **Classifies** the complaint into a database enum category + priority.
4. **Decides** what to do:
   - return a **known resolution** (no ticket needed), or
   - **create a support ticket** and assign the right agent, or
   - **pause for human review** when the complaint is a serious grievance
     (legal threats, repeat failures, etc.).
5. **Responds** to the customer.

The core design principle:

> **The LLM reads and reasons; deterministic code writes.**
> The SQL agent is restricted to read-only `SELECT` queries. All inserts
> (ticket creation) go through parameterized repository code, so the model can
> never corrupt or drop data.

This makes the project a good teaching example of: read-side vs. write-side
separation, LangGraph state machines, conditional routing, and
**human-in-the-loop (HITL)** with `interrupt()` / `Command(resume=...)`.

---

## Architecture

```text
User UI / API
   ↓
FastAPI (main.py)
   ↓
LangGraph workflow (graph.py)
   ↓
Nodes (nodes.py):
   1. understand_complaint   – summarize the complaint
   2. sql_knowledge          – ask the read-only SQL agent for known resolutions
   3. classify_complaint     – map to a DB enum category + priority
   4. decide_next_action     – known_resolution | create_ticket | human_review
   5. human_review           – interrupt() for serious grievances (HITL)
   6. create_ticket          – safe, parameterized INSERT (ticket_repository.py)
   7. *_response             – customer-facing reply (state["response"])
```

Routing after `decide_next_action`:

```text
decide_next_action
   ├── known_resolution → known_resolution_response → END
   ├── create_ticket    → create_ticket → ticket_created_response → END
   └── human_review     → human_review → create_ticket → ticket_created_response → END
```

| File | Responsibility |
|------|----------------|
| `utils.py` | **Google GenAI preset** — `get_llm()`, `get_database()`, `get_sql_database_tools()` (Gemini on Vertex AI) |
| `database.py` | SQLAlchemy engine + `execute_one/all/write` (controlled reads/writes) |
| `state.py` | `CustomerCareState` TypedDict + literals |
| `sql_agent_service.py` | Read-only SQL agent (`ask_database`), lazily built on first use |
| `ticket_repository.py` | Safe customer/product/agent lookups + ticket INSERT |
| `nodes.py` | All workflow nodes + `route_after_decision` |
| `graph.py` | `StateGraph` wiring + `InMemorySaver` checkpointer |
| `schemas.py` | FastAPI request/response models |
| `main.py` | FastAPI app (`/api/v1/complaints`, resume endpoint) |
| `customercaredb/init.sql` | Electronics customer-care schema + seed data |
| `docker-compose.yml` | PostgreSQL 16 (+ pgAdmin) |
| `tests/` | pytest suite (unit + FastAPI workflow tests) |

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python project + dependency manager)
- Docker (for PostgreSQL)
- A Google Cloud project with **Vertex AI** enabled, and Application Default
  Credentials configured:
  ```bash
  gcloud auth application-default login
  ```

---

## Setup

### 1. Environment variables (`.env`)

```env
GOOGLE_CLOUD_PROJECT='your-gcp-project'
DATABASE_URL="postgresql://ccuser:ccpassword@localhost:5432/customer_care"
MODEL_NAME="gemini-2.5-flash-lite"
```

### 2. Start PostgreSQL (seeds `init.sql` on first run)

```bash
docker compose up -d
```

Verify the seed data:

```bash
docker exec -it customer-care-db psql -U ccuser -d customer_care -c "SELECT count(*) FROM tickets;"
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Run the API

```bash
uv run fastapi dev main.py
```

Open the interactive docs at <http://127.0.0.1:8000/docs>.

---

## API reference & sample requests/responses

### `GET /` — health check

```json
{ "status": "ok" }
```

### `POST /api/v1/complaints`

Request body (`ComplaintRequest`):

| Field | Type | Required | Default |
|-------|------|----------|---------|
| `customer_email` | string | no | `null` |
| `customer_name` | string | no | `null` |
| `product_hint` | string | no | `null` |
| `complaint_text` | string | **yes** | – |
| `channel` | string | no | `"chat"` |

#### Example 1 — Known issue (returns a resolution, no ticket)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "sneha.reddy@email.com",
    "product_hint": "Sony WH-1000XM5",
    "complaint_text": "My Sony WH-1000XM5 headphones are not pairing with my Dell laptop.",
    "channel": "chat"
  }'
```

```json
{
  "thread_id": "0f7c...e91",
  "status": "completed",
  "response": "I found a similar known issue and resolution.\n\n...\n\nIf this does not solve your issue, please ask me to create a support ticket.",
  "ticket_ref": null,
  "interrupted": false,
  "review_payload": null
}
```

#### Example 2 — New issue (creates a ticket)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "rahul.mehta@email.com",
    "product_hint": "Samsung T7 SSD",
    "complaint_text": "My Samsung T7 Portable SSD is not detected on Windows 11.",
    "channel": "chat"
  }'
```

```json
{
  "thread_id": "a31b...4c2",
  "status": "completed",
  "response": "Your support ticket has been created.\n\nTicket Reference: TKT-2026-00011\nCategory: product_defect\nPriority: high\nAssigned Agent: naveen.raj@support.com\n\nOur support team will review this and get back to you.",
  "ticket_ref": "TKT-2026-00011",
  "interrupted": false,
  "review_payload": null
}
```

#### Example 3 — Serious grievance (pauses for human review)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "vikram.patel@email.com",
    "product_hint": "iPad Pro",
    "complaint_text": "My iPad Pro arrived with a cracked screen. I complained many times and will go to consumer court.",
    "channel": "email"
  }'
```

```json
{
  "thread_id": "c5d2...77a",
  "status": "human_review_required",
  "response": null,
  "ticket_ref": null,
  "interrupted": true,
  "review_payload": [
    {
      "value": {
        "reason": "Customer complaint contains serious escalation language.",
        "category": "shipping_damage",
        "priority": "critical",
        "complaint_text": "My iPad Pro arrived with a cracked screen...",
        "suggested_action": "Approve critical ticket creation and escalation."
      }
    }
  ]
}
```

### `POST /api/v1/reviews/{thread_id}/resume`

Resume a paused workflow using the `thread_id` from Example 3.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/reviews/c5d2...77a/resume \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "approve_escalation",
    "comments": "Valid serious grievance. Create critical ticket and escalate."
  }'
```

```json
{
  "status": "resumed",
  "response": "Your grievance has been reviewed and registered as a critical support case.\n\nTicket Reference: TKT-2026-00012\nCategory: shipping_damage\nPriority: critical\nAssigned Agent: aditya.singh@support.com\nHuman Review Decision: approve_escalation\nReviewer Comments: Valid serious grievance. Create critical ticket and escalate.\n\nA senior support representative will handle this case.",
  "ticket_ref": "TKT-2026-00012",
  "debug": { "...": "per-node trace" }
}
```

> Resuming a `thread_id` that is not paused for review returns **404**
> (`No interrupted workflow found for this thread_id.`).

---

## Debugging in VS Code

A ready-to-use [`.vscode/launch.json`](.vscode/launch.json) is included with three
configurations.

### 1. Select the interpreter

`Ctrl+Shift+P` → **Python: Select Interpreter** → choose the project venv
(`.venv\Scripts\python.exe`). All configs below assume it.

### 2. Launch configurations

| Configuration | What it does |
|---------------|--------------|
| **FastAPI: debug server** | Runs `uvicorn main:app --reload` under the debugger. Set breakpoints in `main.py`, `nodes.py`, `graph.py`, then hit the API from `/docs` or curl. |
| **Pytest: current file** | Debugs the test file currently open in the editor. |
| **Pytest: all tests** | Debugs the whole suite. |

Press `F5`, pick a configuration, and set breakpoints in the gutter.

### Tips

- The configs load `.env` automatically via `envFile`, so
  `GOOGLE_CLOUD_PROJECT` / `DATABASE_URL` are available.
- To debug the workflow logic **without** the LLM/DB, put a breakpoint in a
  node and run the **Pytest** config — the tests fake `ask_database` and
  `create_ticket`, so you step through real graph routing deterministically.
- If your VS Code workspace root is a parent folder (the monorepo), adjust each
  config's `cwd` to this project directory.
- Use the **Testing** panel (beaker icon) to run/debug individual tests once the
  Python extension discovers them.

---

## Running unit tests

The suite is **hermetic**: the Gemini SQL agent (`nodes.ask_database`) and the
PostgreSQL write (`nodes.create_ticket`) are mocked in `tests/conftest.py`, so
tests are fast and need **no database or Google Cloud credentials**.

```bash
# all tests
uv run pytest

# verbose
uv run pytest -v

# a single file / test
uv run pytest tests/test_api_workflow.py
uv run pytest tests/test_api_workflow.py::test_new_issue_creates_ticket

# with coverage (after: uv add --dev pytest-cov)
uv run pytest --cov=. --cov-report=term-missing
```

What's covered:

| File | Scope |
|------|-------|
| `tests/test_logic.py` | Pure unit tests for `classify_complaint`, `decide_next_action`, `route_after_decision` (no mocks). |
| `tests/test_api_workflow.py` | The real graph driven through FastAPI `TestClient`: health, known-issue, new-issue, grievance interrupt, interrupt→resume, and unknown-thread 404. |

> These do not call Vertex AI. To smoke-test the **real** LLM + DB path, run the
> app (`uv run fastapi dev main.py`) with Docker up and credentials configured,
> then use the sample requests above.

---

## Best practices used here

- **Read/write separation.** The LLM SQL agent is `SELECT`-only (enforced by the
  system prompt); all mutations go through `ticket_repository.py`.
- **Parameterized SQL.** Every query uses bound parameters (`:name`) — never
  string interpolation — to avoid SQL injection.
- **Deterministic classification & routing.** Category/priority/escalation are
  rule-based and unit-tested, so routing is predictable and cheap.
- **Lazy, side-effect-free imports.** The SQL agent is built on first use
  (`get_sql_agent()`), so importing the app needs no live DB — better startup
  and testable modules.
- **Human-in-the-loop for serious cases.** `interrupt()` pauses the graph and
  persists state via the checkpointer; `Command(resume=...)` continues it,
  keyed by `thread_id`.
- **Typed boundaries.** Pydantic models validate API I/O; `CustomerCareState`
  documents the graph contract.
- **Robust endpoints.** Resuming an unknown/non-paused thread returns a clean
  `404` instead of a 500.
- **Config via environment.** No secrets or connection strings in code; `.env`
  drives DB + model selection.

---

## Possible next enhancements

1. **Structured SQL-agent output.** Have `ask_database` return JSON
   (`known_resolution_found`, `similar_ticket_ref`, ...) instead of free text,
   and parse it — removes the brittle `"known_resolution_found: yes"` string
   check.
2. **Better product matching.** Replace `LIKE` matching with embeddings /
   full-text search over the product catalog.
3. **Durable checkpointer.** Swap `InMemorySaver` for a Postgres checkpointer so
   interrupts survive restarts and scale across workers.
4. **Notifications.** Add the `notify_support_team` service (email / Slack) and
   call it from `create_ticket_node`.
5. **Human-review persistence.** Store review payloads/decisions in a dedicated
   table for audit.
6. **Subgraphs & supervisor.** Split into known-resolution / ticket-creation /
   escalation subgraphs, and add a supervisor routing to specialist agents
   (Product, Billing, Warranty, Escalation).
7. **Streaming + LLM classification.** Stream graph events to the client and
   replace keyword rules with a structured-output LLM classifier.
8. **Frontend.** Add a Streamlit or React UI on top of the API.
9. **Integration test tier.** Add `@pytest.mark.integration` tests that exercise
   the real Gemini + Postgres path, skipped unless creds/DB are present.
10. **Observability.** Enable LangSmith tracing and structured logging.

---

## Notes

- `MODEL_NAME` selects the Gemini model; `utils.py` defaults to
  `gemini-2.5-flash-lite` if it is unset.
- Two harmless warnings may appear in tests: Starlette's `TestClient`
  httpx-deprecation notice and `langchain-community`'s sunset notice from
  `utils.py`.
