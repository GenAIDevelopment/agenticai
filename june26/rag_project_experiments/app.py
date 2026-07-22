import streamlit as st

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

load_dotenv()

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Gemini Chat",
    page_icon="🤖",
    layout="wide",
)

# -------------------------------------------------------
# CSS
# -------------------------------------------------------

st.markdown(
    """
<style>

.block-container{
    max-width:900px;
    padding-top:1rem;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Gemini Model
# -------------------------------------------------------

@st.cache_resource
def get_model_from_gcp(
    model_name: str = "gemini-2.5-flash-lite",
) -> ChatGoogleGenerativeAI:
    """
    Returns a cached Gemini model.
    """

    return ChatGoogleGenerativeAI(
        model=model_name,
    )


# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.title("🤖 Gemini Chat")

    model_name = st.selectbox(
        "Model",
        [
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
        ],
    )

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -------------------------------------------------------
# Load Model
# -------------------------------------------------------

llm = get_model_from_gcp(model_name)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.title("💬 Gemini Assistant")

st.caption("Powered by LangChain + Google Gemini")

# -------------------------------------------------------
# Show Previous Messages
# -------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------------
# Chat Input
# -------------------------------------------------------

prompt = st.chat_input("Ask anything...")

if prompt:

    # ------------------------
    # Save User Message
    # ------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ------------------------
    # Convert History
    # ------------------------

    history = []

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(AIMessage(content=msg["content"]))

    # ------------------------
    # Assistant Response
    # ------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""

        for chunk in llm.stream(history):

            if chunk.content:
                response += chunk.content
                placeholder.markdown(response + "▌")

        placeholder.markdown(response)

    # ------------------------
    # Save Assistant Message
    # ------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )