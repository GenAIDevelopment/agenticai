"""Shared pytest fixtures for the customer care test suite.

The workflow normally talks to two external systems:

* the Gemini SQL agent (via ``nodes.ask_database``), and
* PostgreSQL (via ``nodes.create_ticket``).

These fixtures replace both at the ``nodes`` module boundary so the FastAPI
endpoints and the real LangGraph workflow can be exercised without a live
database or Google Cloud credentials. Tests that want a "known resolution" can
override ``nodes.ask_database`` again with ``monkeypatch``.

Note: the node functions look up ``ask_database`` / ``create_ticket`` as module
globals at call time, so patching ``nodes.<name>`` affects the already-compiled
graph used by the app.
"""

import pytest
from fastapi.testclient import TestClient

import main
import nodes

# Deterministic ticket returned by the mocked repository.
FAKE_TICKET = {
    "ticket_id": 999,
    "ticket_ref": "TKT-TEST-00999",
    "assigned_agent_email": "tier2.agent@support.com",
}

# Default SQL-agent answer: no known resolution found.
NO_KNOWN_RESOLUTION = "known_resolution_found: no\nsupport_notes: nothing on file"


@pytest.fixture
def created_tickets():
    """Records the keyword arguments of every ``create_ticket`` call."""
    return []


@pytest.fixture(autouse=True)
def isolate_workflow(monkeypatch, created_tickets):
    """Replace the LLM and DB boundaries with deterministic fakes.

    Applied to every test automatically. Individual tests may re-patch
    ``nodes.ask_database`` to simulate a known resolution.
    """

    def fake_create_ticket(**kwargs):
        """Record the call and return a fixed ticket instead of writing to the DB."""
        created_tickets.append(kwargs)
        return dict(FAKE_TICKET)

    monkeypatch.setattr(nodes, "ask_database", lambda question: NO_KNOWN_RESOLUTION)
    monkeypatch.setattr(nodes, "create_ticket", fake_create_ticket)
    return monkeypatch


@pytest.fixture
def client():
    """A FastAPI ``TestClient`` bound to the real app."""
    with TestClient(main.app) as test_client:
        yield test_client
