import streamlit as st
import ollama

st.title(" Llama3 (8b) Chatbot")

if "messaages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I am Llama3 (8b) Chatbot. How can I help you today?"}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="\U0001f600").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="\U0001f916").write(msg["content"])

def generate_response():
    response = ollama.chat(model='llama3:8b', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="\U0001f600").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="\U0001f916").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})