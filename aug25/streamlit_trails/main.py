import streamlit as st
import time

st.title("Devil Bot 🤖")

def gen_ai_response(prompt: str) -> str:
    """simulates ai response

    Args:
        prompt (str): _description_

    Returns:
        str: _description_
    """
    time.sleep(5)
    return f"I see. You said {prompt}  "

user_prompt = st.text_input(" 😈😈😈  What's on your mind ? 😈😈😈")
if st.button("😈 Get Devils respose 😈"):
    with st.spinner("Devil is thinking 🤔"):
        response = gen_ai_response(user_prompt)
    st.write(response)
