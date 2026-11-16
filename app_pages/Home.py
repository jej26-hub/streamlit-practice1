
import base64
import streamlit as st

client = st.session_state.get("openai_client")


question = st.text_input("질문을 입력하세요")


@st.cache_data
def get_response(question, api_key, _client):
    response = _client.responses.create(
        model="gpt-6-luna",
        input=question
    )
    return response.output_text


if st.button("질문하기"):
    if client is None:
        st.warning("사이드바에 API Key를 입력하세요.")
    elif not question.strip():
        st.warning("질문을 입력하세요.")
    else:
        answer = get_response(
            question.strip(),
            client.api_key,
            client
        )
        st.write(answer)


st.subheader("AI 이미지 생성")

prompt = st.text_input("이미지 프롬프트를 입력하세요")

if st.button("이미지 생성하기"):
    if client is None:
        st.warning("사이드바에 API Key를 입력하세요.")
    elif not prompt.strip():
        st.warning("이미지 프롬프트를 입력하세요.")
    else:
        with st.spinner("이미지 생성 중..."):
            img = client.images.generate(
                model="gpt-image-2.6-flare",
                prompt=prompt.strip()
            )

            image_bytes = base64.b64decode(
                img.data[0].b64_json
            )

        st.image(image_bytes)
