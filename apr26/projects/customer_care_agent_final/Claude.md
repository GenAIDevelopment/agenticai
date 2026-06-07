Below is a **step-by-step build plan with “why we are doing it” first, then code**. We will build a practical MVP using:

```text
LangGraph + LangChain SQLDatabaseToolkit + FastAPI + PostgreSQL + uv
```

We will use the database from your GitHub `init.sql`. That schema is already designed for **electronics customer care** with products, customers, agents, tickets, resolutions, comments, enums, and reporting views. The schema includes ticket status, priority, category, and channel enums; products; customers; agents; tickets; resolutions; and views for ticket overview, resolution summary, and agent performance. ([GitHub][1])

LangChain’s SQL toolkit is useful here because it allows an agent to inspect tables, fetch schemas, generate SQL, run queries, recover from SQL errors, and formulate answers from database results. LangChain also warns that model-generated SQL has risks, so we should scope database permissions narrowly and avoid giving the agent write access directly. ([LangChain Docs][2])

---

# 0. MVP Architecture

```text
User UI / API
   ↓
FastAPI
   ↓
LangGraph Workflow
   ↓
Nodes:
   1. Understand complaint
   2. Ask DB using SQLDatabaseToolkit
   3. Classify issue
   4. Decide known issue / new ticket / serious grievance
   5. Human review if serious
   6. Create ticket using safe service code
   7. Respond to user
```

Important design decision:

```text
Use SQLDatabaseToolkit mostly for READ operations.
Use normal Python service functions for INSERT / UPDATE.
```

Why?

Because SQLDatabaseToolkit can execute model-generated SQL. That is powerful but risky. For production-like design, let the LLM **read and reason**, but let your application code perform controlled writes.

---

# 1. Create Project with uv

## Why

We use `uv` because it manages dependencies, virtual environment, lock file, and running commands in one workflow. The uv FastAPI guide recommends `uv init --app`, `uv add fastapi --extra standard`, and `uv run fastapi dev` for running the app. ([Astral Docs][3])

## Commands

```bash
mkdir customer-care-langgraph
cd customer-care-langgraph

uv init --app
```

Add dependencies:

```bash
uv add fastapi --extra standard
uv add langgraph langchain langchain-community langchain-openai
uv add sqlalchemy psycopg2-binary python-dotenv pydantic
uv add requests
```

For development:

```bash
uv add --dev pytest
```

---

# 2. Folder Structure

## Why

We separate graph, nodes, database, services, and API so students can understand the architecture clearly.

```text
customer-care-langgraph/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── main_graph.py
│   │   └── routing.py
│   │
│   ├── nodes/
│   │   ├── understand_complaint.py
│   │   ├── sql_knowledge_node.py
│   │   ├── classify_complaint.py
│   │   ├── decide_next_action.py
│   │   ├── create_ticket_node.py
│   │   ├── human_review_node.py
│   │   └── response_node.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── ticket_repository.py
│   │
│   ├── services/
│   │   ├── sql_agent_service.py
│   │   └── notification_service.py
│   │
│   └── schemas/
│       └── complaint_schema.py
│
├── customercaredb/
│   └── init.sql
│
├── docker-compose.yml
├── .env
├── pyproject.toml
└── README.md
```

Create folders:

```bash
mkdir -p app/graph app/nodes app/db app/services app/schemas customercaredb
touch app/__init__.py app/graph/__init__.py app/nodes/__init__.py
touch app/db/__init__.py app/services/__init__.py app/schemas/__init__.py
```

---

# 3. Add Database SQL File

## Why

The project should start with your existing schema and seed data. This gives us realistic support data for known issues and known resolutions.

Download your SQL file:

```bash
curl -L \
https://raw.githubusercontent.com/GenAIDevelopment/agenticai/refs/heads/main/apr26/projects/customer_care_agent/customercaredb/init.sql \
-o customercaredb/init.sql
```

---

# 4. Start PostgreSQL with Docker Compose

## Why

Your `init.sql` uses PostgreSQL-specific features like enums and `SERIAL`, so PostgreSQL is better than SQLite for this project.

Create `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:16
    container_name: customer-care-db
    environment:
      POSTGRES_DB: customercare
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./customercaredb/init.sql:/docker-entrypoint-initdb.d/init.sql
```

Run:

```bash
docker compose up -d
```

Check DB:

```bash
docker exec -it customer-care-db psql -U postgres -d customercare
```

Inside psql:

```sql
\dt
SELECT * FROM products LIMIT 5;
SELECT * FROM tickets LIMIT 5;
SELECT * FROM resolutions LIMIT 5;
```

---

# 5. Add Environment Variables

## Why

We do not hardcode DB connection or API keys.

Create `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/customercare

OPENAI_API_KEY=your_openai_key_here

LANGSMITH_TRACING=false
```

You can later switch `OPENAI_API_KEY` to Azure OpenAI, Gemini, or local Ollama-compatible routing depending on your model provider.

---

# 6. Database Connection

## Why

SQLDatabaseToolkit needs a SQLAlchemy connection string. Our write operations also need SQLAlchemy engine or raw SQL execution.

Create `app/db/database.py`:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv()


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is missing in .env")
    return database_url


def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


engine = get_engine()


def execute_one(query: str, params: dict | None = None):
    with engine.begin() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchone()


def execute_all(query: str, params: dict | None = None):
    with engine.begin() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchall()


def execute_write(query: str, params: dict | None = None):
    with engine.begin() as conn:
        result = conn.execute(text(query), params or {})
        try:
            return result.fetchone()
        except Exception:
            return None
```

---

# 7. Define Graph State

## Why

LangGraph is state-based. Every node receives state and returns updates. We keep all workflow information in one state object.

Create `app/graph/state.py`:

```python
from typing import TypedDict, Literal, Optional, Any


Category = Literal[
    "product_defect",
    "warranty_claim",
    "installation_support",
    "software_issue",
    "shipping_damage",
    "returns_refunds",
    "billing",
    "general_inquiry",
]

Priority = Literal["low", "medium", "high", "critical"]

NextAction = Literal[
    "known_resolution",
    "create_ticket",
    "human_review",
    "final_response",
]


class CustomerCareState(TypedDict, total=False):
    # Input
    customer_email: Optional[str]
    customer_name: Optional[str]
    product_hint: Optional[str]
    complaint_text: str
    channel: str

    # Understanding
    issue_summary: Optional[str]
    detected_product: Optional[str]
    customer_intent: Optional[str]

    # Classification
    category: Optional[Category]
    priority: Optional[Priority]
    seriousness_reason: Optional[str]
    escalation_required: bool

    # SQL knowledge
    sql_answer: Optional[str]
    known_resolution_found: bool
    known_resolution: Optional[str]
    similar_ticket: Optional[str]

    # Ticket
    ticket_required: bool
    ticket_id: Optional[int]
    ticket_ref: Optional[str]
    assigned_agent_email: Optional[str]

    # Human review
    human_review_required: bool
    human_decision: Optional[str]
    human_comments: Optional[str]

    # Routing
    next_action: Optional[NextAction]

    # Final
    response: Optional[str]
    debug: dict[str, Any]
```

---

# 8. Create SQLDatabaseToolkit Service

## Why

Instead of writing many SQL queries manually, we allow the agent to use database tools to answer questions like:

```text
Do we have a known resolution for Sony WH-1000XM5 pairing issue?
Find similar resolved tickets.
Which product does this complaint refer to?
Which agent should handle this category?
```

LangChain’s SQL agent tutorial describes the general flow: inspect tables, decide relevant tables, fetch schema, generate SQL, double-check, execute, recover from errors, and formulate a response. ([LangChain Docs][4])

Create `app/services/sql_agent_service.py`:

```python
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

from app.db.database import get_database_url

load_dotenv()


def build_sql_agent():
    db = SQLDatabase.from_uri(get_database_url())

    llm = init_chat_model(
        "openai:gpt-4.1-mini",
        temperature=0,
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    system_prompt = """
You are a customer care database assistant.

You can read the customer care database to help a support workflow.

Database domain:
- Electronics products
- Customers
- Agents
- Support tickets
- Ticket resolutions
- Ticket comments
- Reporting views

Your job:
1. Find matching products.
2. Find similar resolved tickets.
3. Find known resolutions.
4. Find suitable support agents.
5. Summarize findings clearly.

Important rules:
- Prefer SELECT queries only.
- Do not INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
- If you need to create or update a ticket, say that the application should do it.
- Limit results to at most 5 rows unless asked otherwise.
- When searching for known resolutions, prefer resolved tickets joined with resolutions.
- Return concise, structured answers.
"""

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )


sql_agent = build_sql_agent()


def ask_database(question: str) -> str:
    result = sql_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    return result["messages"][-1].content
```

Important teaching point:

```text
SQLDatabaseToolkit is used as a read-side intelligence layer.
Ticket creation is handled by deterministic repository code.
```

---

# 9. Node 1 — Understand Complaint

## Why

Before DB lookup, we convert raw complaint into a useful summary. In MVP, use rules. Later, replace with structured LLM output.

Create `app/nodes/understand_complaint.py`:

```python
from app.graph.state import CustomerCareState


def understand_complaint(state: CustomerCareState) -> CustomerCareState:
    complaint = state["complaint_text"]

    product_hint = state.get("product_hint")
    detected_product = product_hint

    issue_summary = complaint.strip()[:300]

    return {
        **state,
        "issue_summary": issue_summary,
        "detected_product": detected_product,
        "debug": {
            **state.get("debug", {}),
            "understand_complaint": "Complaint summarized",
        },
    }
```

---

# 10. Node 2 — Ask DB for Known Resolution

## Why

This is where SQLDatabaseToolkit adds value. We ask the agent to inspect tickets and resolutions and find similar resolved cases.

Create `app/nodes/sql_knowledge_node.py`:

```python
from app.graph.state import CustomerCareState
from app.services.sql_agent_service import ask_database


def sql_knowledge_node(state: CustomerCareState) -> CustomerCareState:
    complaint = state["complaint_text"]
    product_hint = state.get("product_hint") or "not provided"

    question = f"""
A customer has the following complaint:

Complaint:
{complaint}

Product hint:
{product_hint}

Find whether this is a known issue with a known resolution.

Use the database tables and views.
Look for:
- matching product
- similar resolved tickets
- resolution summary
- root cause
- action taken

Return:
known_resolution_found: yes/no
similar_ticket_ref: value if available
known_resolution: short practical answer for customer
support_notes: short internal notes
"""

    answer = ask_database(question)

    known_resolution_found = "known_resolution_found: yes" in answer.lower()

    return {
        **state,
        "sql_answer": answer,
        "known_resolution_found": known_resolution_found,
        "known_resolution": answer if known_resolution_found else None,
        "debug": {
            **state.get("debug", {}),
            "sql_knowledge_node": answer,
        },
    }
```

Note: this string check is simple for MVP. Later, make the SQL agent return structured JSON.

---

# 11. Node 3 — Classify Complaint

## Why

The DB has enum categories. We should classify into exactly those categories so ticket insert does not fail.

Create `app/nodes/classify_complaint.py`:

```python
from app.graph.state import CustomerCareState


def classify_complaint(state: CustomerCareState) -> CustomerCareState:
    text = state["complaint_text"].lower()

    category = "general_inquiry"
    priority = "medium"
    escalation_required = False
    seriousness_reason = None

    if any(word in text for word in ["not working", "defect", "broken", "dead pixel", "overheating", "not detected"]):
        category = "product_defect"
        priority = "high"

    if any(word in text for word in ["warranty", "replacement", "guarantee"]):
        category = "warranty_claim"
        priority = "high"

    if any(word in text for word in ["install", "installation", "setup", "mount"]):
        category = "installation_support"
        priority = "medium"

    if any(word in text for word in ["software", "firmware", "update", "bluetooth", "pairing", "app", "driver"]):
        category = "software_issue"
        priority = "medium"

    if any(word in text for word in ["cracked", "shipping damage", "damaged delivery", "delivered damaged"]):
        category = "shipping_damage"
        priority = "critical"

    if any(word in text for word in ["return", "refund", "money back"]):
        category = "returns_refunds"
        priority = "high"

    if any(word in text for word in ["invoice", "billing", "charged", "payment", "amount deducted"]):
        category = "billing"
        priority = "medium"

    serious_words = [
        "consumer court",
        "legal",
        "police",
        "fraud",
        "repeated",
        "many times",
        "third time",
        "business loss",
        "urgent escalation",
    ]

    if any(word in text for word in serious_words):
        priority = "critical"
        escalation_required = True
        seriousness_reason = "Customer complaint contains serious escalation language."

    return {
        **state,
        "category": category,
        "priority": priority,
        "escalation_required": escalation_required,
        "human_review_required": escalation_required,
        "seriousness_reason": seriousness_reason,
        "debug": {
            **state.get("debug", {}),
            "classify_complaint": {
                "category": category,
                "priority": priority,
                "escalation_required": escalation_required,
            },
        },
    }
```

---

# 12. Node 4 — Decide Next Action

## Why

LangGraph becomes powerful when we separate decision logic from action logic.

Create `app/nodes/decide_next_action.py`:

```python
from app.graph.state import CustomerCareState


def decide_next_action(state: CustomerCareState) -> CustomerCareState:
    if state.get("escalation_required") or state.get("priority") == "critical":
        next_action = "human_review"
    elif state.get("known_resolution_found"):
        next_action = "known_resolution"
    else:
        next_action = "create_ticket"

    return {
        **state,
        "next_action": next_action,
        "debug": {
            **state.get("debug", {}),
            "decide_next_action": next_action,
        },
    }
```

---

# 13. Routing Function

## Why

Conditional edges decide where the workflow goes next.

Create `app/graph/routing.py`:

```python
from app.graph.state import CustomerCareState


def route_after_decision(state: CustomerCareState) -> str:
    return state["next_action"]
```

---

# 14. Safe Ticket Repository

## Why

We do not let the LLM insert tickets directly. We use safe parameterized SQL from our application.

Create `app/db/ticket_repository.py`:

```python
from app.db.database import execute_one, execute_write


def find_customer_id_by_email(email: str | None) -> int | None:
    if not email:
        return None

    row = execute_one(
        """
        SELECT customer_id
        FROM customers
        WHERE email = :email
        """,
        {"email": email},
    )

    return row[0] if row else None


def find_product_id(product_hint: str | None, complaint_text: str) -> int | None:
    search_text = f"{product_hint or ''} {complaint_text}".lower()

    rows = execute_one(
        """
        SELECT product_id, name, brand, model_number
        FROM products
        WHERE LOWER(name) LIKE :q
           OR LOWER(brand) LIKE :q
           OR LOWER(model_number) LIKE :q
        LIMIT 1
        """,
        {"q": f"%{search_text[:40]}%"},
    )

    if rows:
        return rows[0]

    # fallback: scan products
    from app.db.database import execute_all

    products = execute_all(
        """
        SELECT product_id, name, brand, model_number
        FROM products
        """
    )

    for product_id, name, brand, model_number in products:
        candidates = [name, brand, model_number]
        for candidate in candidates:
            if candidate and candidate.lower() in search_text:
                return product_id

    return None


def find_agent_id_for_category(category: str, priority: str) -> tuple[int | None, str | None]:
    if priority == "critical":
        department = "Escalations"
    elif category in ["product_defect", "warranty_claim", "software_issue"]:
        department = "Tier 2 Support"
    else:
        department = "Tier 1 Support"

    row = execute_one(
        """
        SELECT agent_id, email
        FROM agents
        WHERE department = :department
        ORDER BY agent_id
        LIMIT 1
        """,
        {"department": department},
    )

    if not row:
        return None, None

    return row[0], row[1]


def get_next_ticket_ref() -> str:
    row = execute_one("SELECT COUNT(*) FROM tickets")
    next_number = row[0] + 1
    return f"TKT-2026-{next_number:05d}"


def create_ticket(
    customer_email: str | None,
    product_hint: str | None,
    complaint_text: str,
    channel: str,
    category: str,
    priority: str,
) -> dict:
    customer_id = find_customer_id_by_email(customer_email)
    product_id = find_product_id(product_hint, complaint_text)
    agent_id, agent_email = find_agent_id_for_category(category, priority)
    ticket_ref = get_next_ticket_ref()

    subject = complaint_text[:120]

    row = execute_write(
        """
        INSERT INTO tickets (
            ticket_ref,
            customer_id,
            product_id,
            agent_id,
            channel,
            category,
            priority,
            status,
            subject,
            description
        )
        VALUES (
            :ticket_ref,
            :customer_id,
            :product_id,
            :agent_id,
            :channel,
            :category,
            :priority,
            'open',
            :subject,
            :description
        )
        RETURNING ticket_id
        """,
        {
            "ticket_ref": ticket_ref,
            "customer_id": customer_id,
            "product_id": product_id,
            "agent_id": agent_id,
            "channel": channel,
            "category": category,
            "priority": priority,
            "subject": subject,
            "description": complaint_text,
        },
    )

    return {
        "ticket_id": row[0],
        "ticket_ref": ticket_ref,
        "assigned_agent_email": agent_email,
    }
```

---

# 15. Ticket Creation Node

## Why

The graph node calls the safe repository function.

Create `app/nodes/create_ticket_node.py`:

```python
from app.graph.state import CustomerCareState
from app.db.ticket_repository import create_ticket


def create_ticket_node(state: CustomerCareState) -> CustomerCareState:
    ticket = create_ticket(
        customer_email=state.get("customer_email"),
        product_hint=state.get("product_hint"),
        complaint_text=state["complaint_text"],
        channel=state.get("channel", "chat"),
        category=state.get("category", "general_inquiry"),
        priority=state.get("priority", "medium"),
    )

    return {
        **state,
        "ticket_required": False,
        "ticket_id": ticket["ticket_id"],
        "ticket_ref": ticket["ticket_ref"],
        "assigned_agent_email": ticket["assigned_agent_email"],
        "debug": {
            **state.get("debug", {}),
            "create_ticket_node": ticket,
        },
    }
```

---

# 16. Human Review Node

## Why

Serious grievances should not be fully automated. LangGraph interrupts allow us to pause at runtime and wait for external human input. LangGraph docs explain that `interrupt()` pauses graph execution, saves state through the persistence layer, and resumes with `Command(resume=...)`; a checkpointer and `thread_id` are needed. ([LangChain Docs][5])

Create `app/nodes/human_review_node.py`:

```python
from langgraph.types import interrupt
from app.graph.state import CustomerCareState


def human_review_node(state: CustomerCareState) -> CustomerCareState:
    review_payload = {
        "reason": state.get("seriousness_reason"),
        "category": state.get("category"),
        "priority": state.get("priority"),
        "complaint_text": state.get("complaint_text"),
        "sql_findings": state.get("sql_answer"),
        "suggested_action": "Approve critical ticket creation and escalation.",
    }

    decision = interrupt(review_payload)

    return {
        **state,
        "human_decision": decision.get("decision"),
        "human_comments": decision.get("comments"),
        "debug": {
            **state.get("debug", {}),
            "human_review_node": decision,
        },
    }
```

---

# 17. Response Node

## Why

All paths should end with a clear customer-facing response.

Create `app/nodes/response_node.py`:

```python
from app.graph.state import CustomerCareState


def known_resolution_response_node(state: CustomerCareState) -> CustomerCareState:
    response = f"""
I found a similar known issue and resolution.

{state.get("known_resolution")}

If this does not solve your issue, please ask me to create a support ticket.
""".strip()

    return {
        **state,
        "response": response,
    }


def ticket_created_response_node(state: CustomerCareState) -> CustomerCareState:
    response = f"""
Your support ticket has been created.

Ticket Reference: {state.get("ticket_ref")}
Category: {state.get("category")}
Priority: {state.get("priority")}
Assigned Agent: {state.get("assigned_agent_email")}

Our support team will review this and get back to you.
""".strip()

    return {
        **state,
        "response": response,
    }


def escalation_response_node(state: CustomerCareState) -> CustomerCareState:
    response = f"""
Your grievance has been reviewed and registered as a critical support case.

Ticket Reference: {state.get("ticket_ref")}
Category: {state.get("category")}
Priority: {state.get("priority")}
Human Review Decision: {state.get("human_decision")}
Reviewer Comments: {state.get("human_comments")}

A senior support representative will handle this case.
""".strip()

    return {
        **state,
        "response": response,
    }
```

---

# 18. Build LangGraph

## Why

Now we wire nodes into a workflow.

LangGraph interrupts require a checkpointer and a thread id to resume. For MVP, we use `InMemorySaver`; for production, use a durable checkpointer. The LangGraph docs explicitly recommend a durable checkpointer in production for interrupts. ([LangChain Docs][5])

Create `app/graph/main_graph.py`:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.graph.state import CustomerCareState
from app.graph.routing import route_after_decision

from app.nodes.understand_complaint import understand_complaint
from app.nodes.sql_knowledge_node import sql_knowledge_node
from app.nodes.classify_complaint import classify_complaint
from app.nodes.decide_next_action import decide_next_action
from app.nodes.create_ticket_node import create_ticket_node
from app.nodes.human_review_node import human_review_node
from app.nodes.response_node import (
    known_resolution_response_node,
    ticket_created_response_node,
    escalation_response_node,
)


def build_customer_care_graph():
    builder = StateGraph(CustomerCareState)

    builder.add_node("understand_complaint", understand_complaint)
    builder.add_node("sql_knowledge_node", sql_knowledge_node)
    builder.add_node("classify_complaint", classify_complaint)
    builder.add_node("decide_next_action", decide_next_action)

    builder.add_node("known_resolution_response", known_resolution_response_node)
    builder.add_node("create_ticket", create_ticket_node)
    builder.add_node("human_review", human_review_node)
    builder.add_node("ticket_created_response", ticket_created_response_node)
    builder.add_node("escalation_response", escalation_response_node)

    builder.add_edge(START, "understand_complaint")
    builder.add_edge("understand_complaint", "sql_knowledge_node")
    builder.add_edge("sql_knowledge_node", "classify_complaint")
    builder.add_edge("classify_complaint", "decide_next_action")

    builder.add_conditional_edges(
        "decide_next_action",
        route_after_decision,
        {
            "known_resolution": "known_resolution_response",
            "create_ticket": "create_ticket",
            "human_review": "human_review",
        },
    )

    builder.add_edge("known_resolution_response", END)

    builder.add_edge("create_ticket", "ticket_created_response")
    builder.add_edge("ticket_created_response", END)

    builder.add_edge("human_review", "create_ticket")
    builder.add_edge("create_ticket", "ticket_created_response")

    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)


customer_care_graph = build_customer_care_graph()
```

One issue in the above graph: `create_ticket` is used by both normal ticket and escalation flow, but after escalation we may want a different response. For MVP this is acceptable. Later, add a conditional edge after `create_ticket` to choose `ticket_created_response` or `escalation_response`.

---

# 19. FastAPI Schemas

## Why

FastAPI should receive clean request data and return clean response data.

Create `app/schemas/complaint_schema.py`:

```python
from pydantic import BaseModel


class ComplaintRequest(BaseModel):
    customer_email: str | None = None
    customer_name: str | None = None
    product_hint: str | None = None
    complaint_text: str
    channel: str = "chat"


class ComplaintResponse(BaseModel):
    thread_id: str
    status: str
    response: str | None = None
    ticket_ref: str | None = None
    interrupted: bool = False
    review_payload: object | None = None


class HumanReviewRequest(BaseModel):
    decision: str
    comments: str | None = None
```

---

# 20. FastAPI App

## Why

This exposes LangGraph as a REST API.

Create `app/main.py`:

```python
from uuid import uuid4

from fastapi import FastAPI
from langgraph.types import Command

from app.graph.main_graph import customer_care_graph
from app.schemas.complaint_schema import (
    ComplaintRequest,
    ComplaintResponse,
    HumanReviewRequest,
)

app = FastAPI(title="Customer Care LangGraph Agent")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/complaints", response_model=ComplaintResponse)
def submit_complaint(request: ComplaintRequest):
    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    initial_state = {
        "customer_email": request.customer_email,
        "customer_name": request.customer_name,
        "product_hint": request.product_hint,
        "complaint_text": request.complaint_text,
        "channel": request.channel,
        "known_resolution_found": False,
        "ticket_required": True,
        "escalation_required": False,
        "human_review_required": False,
        "debug": {},
    }

    result = customer_care_graph.invoke(initial_state, config=config)

    if "__interrupt__" in result:
        return ComplaintResponse(
            thread_id=thread_id,
            status="human_review_required",
            interrupted=True,
            review_payload=result["__interrupt__"],
        )

    return ComplaintResponse(
        thread_id=thread_id,
        status="completed",
        response=result.get("response"),
        ticket_ref=result.get("ticket_ref"),
        interrupted=False,
    )


@app.post("/api/v1/reviews/{thread_id}/resume")
def resume_review(thread_id: str, request: HumanReviewRequest):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    result = customer_care_graph.invoke(
        Command(
            resume={
                "decision": request.decision,
                "comments": request.comments,
            }
        ),
        config=config,
    )

    return {
        "status": "resumed",
        "response": result.get("response"),
        "ticket_ref": result.get("ticket_ref"),
        "debug": result.get("debug"),
    }
```

---

# 21. Run the API

## Why

We test the backend before adding frontend.

Run:

```bash
uv run fastapi dev app/main.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 22. Test Case 1 — Known Issue

## Why

This validates SQLDatabaseToolkit can search previous resolved tickets and resolutions.

Request:

```json
{
  "customer_email": "sneha.reddy@email.com",
  "product_hint": "Sony WH-1000XM5",
  "complaint_text": "My Sony WH-1000XM5 headphones are not pairing with my Dell laptop.",
  "channel": "chat"
}
```

Expected behavior:

```text
Graph receives complaint
SQLDatabaseToolkit searches products, tickets, resolutions
Known resolution found
No ticket created
Customer gets guidance
```

---

# 23. Test Case 2 — New Issue

Request:

```json
{
  "customer_email": "rahul.mehta@email.com",
  "product_hint": "Samsung T7 SSD",
  "complaint_text": "My Samsung T7 Portable SSD is not detected on Windows 11.",
  "channel": "chat"
}
```

Expected behavior:

```text
Known resolution may not be found
Classify as product_defect or software_issue
Create ticket
Assign Tier 2 agent
Return ticket reference
```

---

# 24. Test Case 3 — Serious Grievance

Request:

```json
{
  "customer_email": "vikram.patel@email.com",
  "product_hint": "iPad Pro",
  "complaint_text": "My iPad Pro arrived with a cracked screen. I complained many times and will go to consumer court.",
  "channel": "email"
}
```

Expected behavior:

```text
Classify as shipping_damage
Priority critical
Graph interrupts for human review
API returns human_review_required
```

Resume request:

```json
{
  "decision": "approve_escalation",
  "comments": "Valid serious grievance. Create critical ticket and escalate."
}
```

---

# 25. Important Fix for Interrupt Response

Depending on LangGraph version and invocation style, interrupt data may appear differently. If `__interrupt__` does not appear in `result`, use streaming later. For learning, start with `invoke`, then improve to streaming.

The conceptual rule remains:

```text
interrupt() pauses
checkpointer stores state
thread_id identifies the paused workflow
Command(resume=...) continues it
```

This is exactly the pattern described in LangGraph’s interrupt docs. ([LangChain Docs][5])

---

# 26. Add Simple Notification Service Later

## Why

For MVP, print notification. Later use email and Slack.

Create `app/services/notification_service.py`:

```python
def notify_support_team(ticket_ref: str, assigned_agent_email: str | None, message: str):
    print("---- SUPPORT NOTIFICATION ----")
    print(f"Ticket: {ticket_ref}")
    print(f"Agent: {assigned_agent_email}")
    print(message)
    print("------------------------------")
```

Then call this from `create_ticket_node`.

---

# 27. What Students Learn from This Version

This version teaches:

```text
1. uv project setup
2. FastAPI API development
3. PostgreSQL schema usage
4. LangChain SQLDatabaseToolkit
5. Read-side database agent
6. Safe write-side repository
7. LangGraph StateGraph
8. Conditional routing
9. Known issue handling
10. New ticket creation
11. Serious grievance detection
12. Human-in-the-loop pause/resume
13. REST API exposure
```

---

# 28. Suggested Next Improvements

After MVP works, improve in this order:

```text
1. Make SQL agent return structured JSON
2. Add proper product matching
3. Add Slack notification
4. Add email notification
5. Add human review table
6. Use PostgreSQL checkpointer instead of InMemorySaver
7. Add subgraphs:
   - known resolution subgraph
   - ticket creation subgraph
   - escalation subgraph
8. Add supervisor:
   - Product Support Agent
   - Billing Agent
   - Warranty Agent
   - Escalation Agent
9. Add Streamlit or React frontend
10. Deploy LangGraph as a separate service and call using langgraph-client
```

---

# 29. One Important Teaching Point

Do not present SQLDatabaseToolkit as “just another database library.”

Teach it this way:

```text
SQLAlchemy/repository code:
Used when our application knows exactly what to do.
Example: create ticket, update ticket, assign agent.

SQLDatabaseToolkit:
Used when the agent needs to explore the database and reason.
Example: find similar resolved tickets, summarize known resolution, inspect support history.
```

That separation makes the design safer, cleaner, and more production-like.

[1]: https://raw.githubusercontent.com/GenAIDevelopment/agenticai/refs/heads/main/apr26/projects/customer_care_agent/customercaredb/init.sql "raw.githubusercontent.com"
[2]: https://docs.langchain.com/oss/python/integrations/tools/sql_database "SQLDatabase toolkit integration - Docs by LangChain"
[3]: https://docs.astral.sh/uv/guides/integration/fastapi/ "Using uv with FastAPI | uv"
[4]: https://docs.langchain.com/oss/python/langchain/sql-agent "Build a SQL agent - Docs by LangChain"
[5]: https://docs.langchain.com/oss/python/langgraph/interrupts "Interrupts - Docs by LangChain"
