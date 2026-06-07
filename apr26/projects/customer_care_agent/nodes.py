from state import CustomerCareState
from sql_agent_service import ask_database
from ticket_repoistory import create_ticket
from langgraph.types import interrupt

def understand_complaint(state: CustomerCareState) -> CustomerCareState:
    complaint = state["complaint_text"]
    product_hint = state["product_hint"]
    #todo: detect the right product
    detected_product = product_hint
    #todo: summarize the issue
    issue_summary = complaint.strip()[:300]
    return {
        **state,
        "detected_product": detected_product,
        "issue_summary": issue_summary,
        "debug": {
            **state.get("debug", {}),
            "understand_complaint": { "complaint summarized" }
        }
    }

def sql_knowledge_node(state: CustomerCareState) -> CustomerCareState:
    complaint = state["complaint_text"]
    product_hint = state["product_hint"]
    question = f"""
A customer has a complaint: {complaint}
They mentioned a product: {product_hint}

Find whether this is a known issue with a known resoultion.

Use the database tables and views.
Look for 
- matching product
- similar resolved tickets
- resolution summary
- root cause
- action taken

Return:
known_resolution_found: yes or no
similar_ticket_ref: value if available
known_resolution: short practical answer for the customer
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
            "sql_knowledge_node": { "query executed" }
        }
    }


def classify_complaint(state: CustomerCareState) -> CustomerCareState:
    text = state["complaint_text"].lower()
    category = "general_inquiry"
    priority = "medium"
    escalation_required = False
    seriousness_reason = None
    if any(word in text for word in ["damage", "broken", "defective", "not working"]):
        category = "product_defect"
        priority = "high"
    if any(word in text for word in ["warranty", "guarantee", "replacement"]):
        category = "warranty_claim"
        priority = "high"
    
    if any(word in text for word in ["install", "setup", "configuration"]):
        category = "installation_support"
        priority = "medium"
    
    if any(word in text for word in ["bug", "error", "crash", "issue", "software", "firmware"]):
            category = "software_issue"
            priority = "high"
            escalation_required = True
            seriousness_reason = "Software issue reported by customer"
        
    if any(word in text for word in ["shipping damage", "broken", "cracked"]):
        category = "shipping_damage"
        priority = "high"
        seriousness_reason = "Customer reports shipping damage"

    if any(word in text for word in ["return", "refund", "exchange"]):
        category = "returns_refunds"
        priority = "high"

    if any(word in text for word in ["invoice", "billing", "charged"]):
        category = "billing"
        priority = "medium"

    serious_words = [
        "consumer court",
        "legal",
        "police",
        "fraud",
        "many times"
    ]
    if any(word in text for word in serious_words):
        escalation_required = True
        seriousness_reason = "Customer mentions legal or serious concerns"
    
    return {
        **state,
        "category": category,
        "priority": priority,
        "escalation_required": escalation_required,
        "seriousness_reason": seriousness_reason,
        "human_review_required": escalation_required,
        "debug": {
            **state.get("debug", {}),
            "classify_complaint": { "complaint classified" }
        }
    }
        

def decide_next_action(state: CustomerCareState) -> CustomerCareState:
    if state["known_resolution_found"]:
        return {
            **state,
            "next_action": "final_response",
            "debug": {
                **state.get("debug", {}),
                "decide_next_action": { "resolution found" }
            }
        }
    elif state["human_review_required"]:
        return {
            **state,
            "next_action": "human_review",
            "debug": {
                **state.get("debug", {}),
                "decide_next_action": { "human review required" }
            }
        }
    else:
        return {
            **state,
            "next_action": "create_ticket",
            "debug": {
                **state.get("debug", {}),
                "decide_next_action": { "ticket creation required" }
            }
        }


def route_after_decision(state: CustomerCareState):
    return state["next_action"]


def create_ticket_node(state: CustomerCareState) -> CustomerCareState:
    customer_email = state["customer_email"]
    product_hint = state["product_hint"]
    complaint_text = state["complaint_text"]
    channel = state["channel"]
    category = state["category"]
    priority = state["priority"]

    ticket_data = create_ticket(
        customer_email=customer_email,
        product_hint=product_hint,
        complaint_text=complaint_text,
        channel=channel,
        category=category,
        priority=priority
    )
    return {
        **state,
        "ticket_required": True,
        "ticket_id": ticket_data["id"],
        "ticket_ref": ticket_data["ref"],
        "debug": {
            **state.get("debug", {}),
            "create_ticket_node": { "ticket created" }
        }
    }


def human_review_node(state: CustomerCareState) -> CustomerCareState:
    review_payload = {
        "reason": state.get("seriousness_reason"),
        "category": state.get("category"),
        "priority": state.get("priority"),
        "complaint_text": state.get("complaint_text"),
        "sql_findings": state.get("sql_answer"),
        "suggested_action": "Approve critical ticket creation and escalation"
    }
    decision = interrupt(review_payload)
    return {
        **state,
        "human_decision": decision.get("decision"),
        "human_comments": decision.get("comments"),
        "debug": {
            **state.get("debug", {}),
            "human_review_node": { "review completed" }
        }
    }


def known_resolution_response_node(state: CustomerCareState) -> CustomerCareState:
    return {
        **state,
        "response_text": state["known_resolution"],
        "debug": {
            **state.get("debug", {}),
            "known_resolution_response_node": { "response generated" }
        }
    }


def ticket_created_response_node(state: CustomerCareState) -> CustomerCareState:
    return {
        **state,
        "response_text": f"Thank you for your patience. We have created ticket {state['ticket_ref']} for your issue. Our support team will contact you shortly.",
        "debug": {
            **state.get("debug", {}),
            "ticket_created_response_node": { "response generated" }
        }
    }

def escalated_response_node(state: CustomerCareState) -> CustomerCareState:
    return {
        **state,
        "response_text": "We have escalated your issue to our senior support team. They will contact you within 2 hours.",
        "debug": {
            **state.get("debug", {}),
            "escalated_response_node": { "response generated" }
        }
    }