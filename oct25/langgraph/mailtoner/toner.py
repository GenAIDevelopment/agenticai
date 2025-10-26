from typing import TypedDict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph
import os

class EmailState(TypedDict):
    draft: str
    tone: str
    mail: str

load_dotenv()
model_name = os.getenv('MODEL_NAME')
model_provider = os.getenv('MODEL_PROVIDER')
llm = init_chat_model(model=model_name, model_provider=model_provider)



def change_email_tone(state: EmailState) -> EmailState:
    draft = state['draft']
    tone = state['tone']
    prompt = ChatPromptTemplate([
        ('system', 'You are an expert email writer'),
        ("user", "Coniser the following draft email {draft} without changing facts and preserving the meaning"),
        ("user", "Rewrite the email in less than 150 words in the following tone {tone}")
    ])
    chain = prompt | llm 
    response = chain.invoke({'draft': draft, 'tone': tone})
    state['mail'] = response.content
    return state

toner_graph = StateGraph(EmailState)
toner_graph.add_node("toner", change_email_tone)
toner_graph.add_edge(START, "toner")
toner_graph.add_edge("toner", END)

graph = toner_graph.compile()
