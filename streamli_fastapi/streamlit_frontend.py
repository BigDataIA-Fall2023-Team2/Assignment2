import streamlit as st
import requests

st.title("FastAPI and Streamlit Interaction")

name = st.text_input("Enter your name:")
btn = st.button("Greet")

if btn:
    if name:
        response = requests.post("http://127.0.0.1:8000/greet/?name="+name)
        if response.status_code == 200:
            greeting = response.json()["message"]
            st.write(f"FastAPI says: {greeting}")
        else:
            st.write("Error in API call.")
    else:
        st.write("Please enter your name.")
