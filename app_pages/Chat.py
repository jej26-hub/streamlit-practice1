
import streamlit as st

client = st.session_state.get("openai_client")


if "messages" not in st.session_state:
    st.session_state.messages = []



def clear_chat():
    st.session_state.messages = []


st.button("Clear", on_click=clear_chat)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    if client is None:
        st.warning("사이드바에 API Key를 입력하세요.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            stream = client.responses.create(
                model="gpt-6-luna",
                input=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
