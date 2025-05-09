import time
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()

client = OpenAI()

if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id = st.session_state.thread_id
assisstant_id = "asst_EQdmL6D58gXo5nYYUscVZrdb"

thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

st.header("강하룡 목사와의 대화")
st.markdown(
    "**_『어떻게 신앙은 성장하는가?』 (브니엘)_** 로 알아보는 신앙 성장에 대한 북 토크"
)

for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)

prompt = st.chat_input("묻고 싶은 내용을 입력하세요!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
    )

    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assisstant_id,
    )

    with st.spinner("응답 기다리는 중..."):
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)
