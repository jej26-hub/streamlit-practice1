
import streamlit as st

client = st.session_state.get("openai_client")

st.title("ChatPDF")

if "chatpdf_messages" not in st.session_state:
    st.session_state["chatpdf_messages"] = []

if "chatpdf_vector_store_id" not in st.session_state:
    st.session_state["chatpdf_vector_store_id"] = None

if "chatpdf_uploader_key" not in st.session_state:
    st.session_state["chatpdf_uploader_key"] = 0


def clear_chatpdf():
    st.session_state["chatpdf_messages"] = []


def leave_chatpdf():
    vector_store_id = st.session_state["chatpdf_vector_store_id"]

    if vector_store_id is not None:
        client.vector_stores.delete(vector_store_id)

    st.session_state["chatpdf_vector_store_id"] = None
    st.session_state["chatpdf_messages"] = []
    st.session_state["chatpdf_uploader_key"] += 1


if st.session_state["chatpdf_vector_store_id"] is None:

    uploaded_file = st.file_uploader(
        "PDF 파일을 업로드하세요",
        type="pdf",
        accept_multiple_files=False,
        key=f"pdf_uploader_{st.session_state['chatpdf_uploader_key']}"
    )

    if uploaded_file is not None:
        if client is None:
            st.warning("사이드바에 OpenAI API Key를 입력하세요.")
        else:
            with st.spinner("PDF 파일을 처리하는 중..."):
                vector_store = client.vector_stores.create()

                vector_store_file = client.vector_stores.files.upload_and_poll(
                    vector_store_id=vector_store.id,
                    file=(uploaded_file.name, uploaded_file.getvalue())
                )

                if vector_store_file.status == "completed":
                    st.session_state["chatpdf_vector_store_id"] = vector_store.id
                else:
                    st.error("PDF 파일 처리에 실패했습니다.")

            if st.session_state["chatpdf_vector_store_id"] is not None:
                st.rerun()

else:
    st.button("Clear", on_click=clear_chatpdf)
    st.button("Leave", on_click=leave_chatpdf)

    for message in st.session_state["chatpdf_messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("PDF에 대해 질문하세요")

    if prompt:
        if client is None:
            st.warning("사이드바에 OpenAI API Key를 입력하세요.")
        else:
            st.session_state["chatpdf_messages"].append({
                "role": "user",
                "content": prompt
            })

            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                stream = client.responses.create(
                    model="gpt-6-luna",
                    input=st.session_state["chatpdf_messages"],
                    tools=[{
                        "type": "file_search",
                        "vector_store_ids": [
                            st.session_state["chatpdf_vector_store_id"]
                        ]
                    }],
                    stream=True
                )

                response = st.write_stream(stream)

            st.session_state["chatpdf_messages"].append({
                "role": "assistant",
                "content": response
            })
