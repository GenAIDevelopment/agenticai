import streamlit as st
import time


st.sidebar.title("Model controls")
st.sidebar.write("Adjust Devils controls here")
evilness = st.sidebar.slider(
    label="Evilness   ",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.1
)
st.sidebar.write(f"Current Evilness: {evilness}")
st.title("Devil Bot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []


def gen_ai_response(prompt: str) -> str:
    """simulates ai response

    Args:
        prompt (str): _description_

    Returns:
        str: _description_
    """
    time.sleep(5)
    return f"I see. You said {prompt}  "

# display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# user_prompt = st.text_input(" 😈😈😈  What's on your mind ? 😈😈😈")
# if st.button("😈 Get Devils respose 😈"):
#     with st.spinner("Devil is thinking 🤔"):
#         response = gen_ai_response(user_prompt)
#     st.write(response)

if user_prompt := st.chat_input(" 😈😈😈  What's on your mind ? 😈😈😈"):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Devil is thinking 🤔"):
            response = gen_ai_response(user_prompt)
            st.markdown(response)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )
            
    

