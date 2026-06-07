"""LangGraph workflow definition for the customer care agent.

Wires the nodes into a state machine:

    START
      -> understand_complaint
      -> sql_knowledge
      -> classify_complaint
      -> decide_next_action
           |-- known_resolution --> known_resolution_response --> END
           |-- create_ticket    --> create_ticket --> ticket_created_response --> END
           |-- human_review     --> human_review --> create_ticket --> ... --> END

Interrupts (human review) require a checkpointer and a ``thread_id``. An
``InMemorySaver`` is used for the MVP; a durable checkpointer should be used in
production.
"""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from nodes import (
    classify_complaint,
    create_ticket_node,
    decide_next_action,
    human_review_node,
    known_resolution_response_node,
    route_after_decision,
    sql_knowledge_node,
    ticket_created_response_node,
    understand_complaint,
)
from state import CustomerCareState


def build_customer_care_graph():
    """Build and compile the customer care workflow graph.

    Returns:
        CompiledStateGraph: Compiled graph with an in-memory checkpointer,
        ready to ``invoke`` with a ``thread_id`` config.
    """
    builder = StateGraph(CustomerCareState)

    builder.add_node("understand_complaint", understand_complaint)
    builder.add_node("sql_knowledge", sql_knowledge_node)
    builder.add_node("classify_complaint", classify_complaint)
    builder.add_node("decide_next_action", decide_next_action)

    builder.add_node("known_resolution_response", known_resolution_response_node)
    builder.add_node("create_ticket", create_ticket_node)
    builder.add_node("human_review", human_review_node)
    builder.add_node("ticket_created_response", ticket_created_response_node)

    builder.add_edge(START, "understand_complaint")
    builder.add_edge("understand_complaint", "sql_knowledge")
    builder.add_edge("sql_knowledge", "classify_complaint")
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

    # Serious grievances are reviewed, then a critical ticket is created.
    builder.add_edge("human_review", "create_ticket")

    builder.add_edge("create_ticket", "ticket_created_response")
    builder.add_edge("ticket_created_response", END)

    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)


customer_care_graph = build_customer_care_graph()
