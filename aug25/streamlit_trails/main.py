import streamlit as st
st.title("Learning stremlit")
st.write("Hello Streamlit")

name = st.text_input("What is your name")

if st.button("Rerun"):
    st.write(f"You clicked me !, kindly stop, otherwise i will scream {name} is cruel")

