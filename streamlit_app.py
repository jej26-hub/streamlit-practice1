
import streamlit as st
from openai import OpenAI

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")

if api_key:
    st.session_state["openai_client"] = OpenAI(api_key=api_key)

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
    st.Page("app_pages/Chatbot.py", title="Chatbot"),
    st.Page("app_pages/ChatPDF.py", title="ChatPDF"),
])
pg.run()
