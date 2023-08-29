import openai
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI

from callback import CustomCallbackHandler

openai.api_key = st.secrets["OPENAI_TOKEN"]

response_llm = ChatOpenAI(
    temperature=0,
    openai_api_key=st.secrets["OPENAI_TOKEN"],
    model_name="gpt-3.5-turbo",
    streaming=True,
    callbacks=[CustomCallbackHandler()]
)

summary_llm = ChatOpenAI(
    temperature=0,
    openai_api_key=st.secrets["OPENAI_TOKEN"],
    model_name="gpt-3.5-turbo",
)

if "chain" not in st.session_state:
    st.session_state.chain = ConversationChain(
        llm=response_llm,
        memory=ConversationSummaryBufferMemory(
            llm=summary_llm,
            max_token_limit=20
        )
    )

st.title("Streamlit Chat💬")

# session state에 대화 내용 저장할 messages list 생성
if "messages" not in st.session_state:
    st.session_state.messages = []

# avatar
user_avatar = "🧑‍💻"
system_avatar = "./images/profile_robot.png"


with st.chat_message(name="system", avatar=system_avatar):
    st.markdown("반갑습니다 휴먼")
    with st.spinner():
        st.image("./images/dance_robot.gif")

# 이전에 나눴던 대화들 차례대로 출력
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    avatar = user_avatar if role == "user" else system_avatar
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

# 유저의 입력 받아서 UI에 추가
prompt = st.chat_input("입력")
if prompt:
    # UI에 그려주기
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)
    # 히스토리에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 답변 생성
    with st.chat_message(name="system", avatar=system_avatar):
        response = st.session_state.chain(prompt)["response"]
    # 히스토리에 추가
    st.session_state.messages.append({"role": "system", "content": response})
