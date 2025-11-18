from langchain_google_vertexai.embeddings import VertexAIEmbeddings
import os
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.postgres import PostgresStore
from dotenv import load_dotenv
from utils import get_llm
from langmem import create_memory_manager, create_memory_store_manager
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.runnables.config import RunnableConfig
from langgraph.store.base import BaseStore
load_dotenv()

model = get_llm()


def get_embedding(name: str = 'text-embedding-005') -> VertexAIEmbeddings:
    return VertexAIEmbeddings(model=name)


class UserPreferences(BaseModel):
    name: str
    city: str
    favorite_drink: str

def ask_llm(
        state: MessagesState,
        config: RunnableConfig,
        *,
        store: BaseStore):
    # 1. Lets identify the user and namespace
    user_id = config["configurable"].get("user_id")
    ns = ("user", user_id, "preferences")

    # 2. Extract and update semantic memory via langmem
    # This updates the store as well
    _ = memory_store_manager.invoke(
        {
            "messages": state["messages"],
            "namespace": ns,
            "config": {"user_id": user_id}
        }
    )

    # 3.  Retrive current profile from store
    results = store.search(
        ns,
        limit=1
    )
    if results:
        profile = results[0].value
        content = profile.get("content")
        name = content.get('name')
        city = content.get('city')
        drink = content.get('favorite_drink')
        parts = []
        if name:
            parts.append(f"Name: {name}")
        if city:
            parts.append(f"City: {city}")
        if drink:
            parts.append(f"Favorite Drink: {drink}")
        profile_text = ", ".join(parts) if parts else "No Profile Details Yet"
    else:
        profile_text = "No Profile Details Yet"

    memories_block = (
        "Here is what you currently know about the user profile: \n",
        f"{profile_text}\n\n"
    )
    system_prompt = (
        "You are a friendly personal assistant. \n",
        "Use the known user profile if it is helpful, but dont invent new facts \n\n",
        f"{memories_block}"
        "Now Continue the conversation"
    )
    response = model.invoke( [ SystemMessage(system_prompt) ] + state['messages'])
    return {
        "messages": [ response ]
    }


stategraph = StateGraph(MessagesState)
stategraph.add_node("ask", ask_llm)
stategraph.set_entry_point("ask")
stategraph.set_finish_point("ask")


if __name__ == "__main__":
    # First converstaion
    with (
            PostgresSaver.from_conn_string(os.getenv('PG_VECTOR_DB_URI')) as saver,
            PostgresStore.from_conn_string(
                os.getenv('PG_VECTOR_DB_URI'),
                index={
                    "dims": 768,
                    "embed": get_embedding(),
                    # specify which fields to embed. Default is the whole serialized value
                    "fields": ["memory_text"]
                }
            ) as store):
        store.setup()
        saver.setup()
        memory_store_manager = create_memory_store_manager(
            model,
            schemas=[UserPreferences],
            store=store,
            namespace=("user", "{user_id}", "preferences"),
            instructions=(
                "Extract and maintain the user's profile information: name, city, favorite_drink.",
                "update existing profile entries when user provides new information."
            ),
            enable_deletes=True,
            enable_inserts=True
        )
        graph = stategraph.compile(checkpointer=saver, store=store)
        response = graph.invoke(
            {
                "messages": [ HumanMessage("Hi Im alice and i like coffee and i live in mumbai")]
            },
            config={
                "configurable": {
                    "thread_id": "t1",
                    "user_id": "alice@wonderland"
                }
            }
        )
        print(response)

        response = graph.invoke(
            {
                "messages": [HumanMessage("What drink do you recommed for me now?")]
            },
            config={
                "configurable": {
                    "thread_id": "t1",
                    "user_id": "alice@wonderland"
                }
            }
        )

        print(response)

        response = graph.invoke(
            {
                "messages": [HumanMessage("What drink do you recommed for me now?")]
            },
            config={
                "configurable": {
                    "thread_id": "t2",
                    "user_id": "alice@wonderland"
                }
            }
        )

        print(response)
