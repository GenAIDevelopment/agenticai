"""LangGraph workflow definition for the customer care agent.

This module defines the customer care workflow as a LangGraph state
machine. The workflow coordinates complaint understanding, knowledge
retrieval, classification, ticket creation, human review, and response
generation.

The compiled graph is exposed as a module-level variable and can be
invoked by application services to process customer support requests.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from state import CustomerCareState
from nodes import (
    route_after_decision,
    understand_complaint,
    sql_knowledge_node,
    classify_complaint,
    create_ticket_node,
    final_response_node,
    human_review_node,
    escalate_for_human_review,
    known_resolution_response_node,
    ticket_created_response_node,
    escalated_response_node,
    decide_next_action,
)


def build_customer_care_graph():
    """Build and compile the customer care workflow graph.

    The workflow performs the following high-level steps:

    1. Understand the customer complaint.
    2. Retrieve relevant information from the database.
    3. Classify the issue and determine priority.
    4. Decide the next workflow action.
    5. Route to resolution, ticket creation, or human review.
    6. Generate a final customer-facing response.

    An in-memory checkpoint saver is configured to support workflow
    state persistence during graph execution.

    Returns:
        CompiledStateGraph: Compiled LangGraph workflow ready for
            execution.
    """
    builder = StateGraph(CustomerCareState)

    builder.add_node("understand_complaint", understand_complaint)
    builder.add_node("sql_knowledge", sql_knowledge_node)
    builder.add_node("classify_complaint", classify_complaint)
    builder.add_node("decide_next_action", decide_next_action)

    builder.add_node(
        "known_resolution_response",
        known_resolution_response_node,
    )
    builder.add_node("create_ticket", create_ticket_node)
    builder.add_node("human_review", human_review_node)
    builder.add_node(
        "ticket_created_response",
        ticket_created_response_node,
    )
    builder.add_node(
        "escalation_response",
        escalated_response_node,
    )

    builder.add_edge(START, "understand_complaint")
    builder.add_edge("understand_complaint", "sql_knowledge")
    builder.add_edge("sql_knowledge", "classify_complaint")

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

    checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)


graph = build_customer_care_graph()