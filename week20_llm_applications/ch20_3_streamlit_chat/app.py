import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_TOKEN"]


def request_chat_completion(messages, stream=False):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=stream
    )
    return response


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
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message(name="system", avatar=system_avatar):
        is_stream = True

        with st.spinner("AI는 고민중..."):
            # time.sleep(1)
            # response = "못알아듣겠습니다 휴먼"

            # chatGPT API
            chatgpt_response = request_chat_completion(
                st.session_state.messages,
                stream=is_stream
            )

        message_placeholder = st.empty()
        if not is_stream:
            response = chatgpt_response["choices"][0]["message"]["content"]
        else:
            response = ""
            for chunk in chatgpt_response:
                delta = chunk.choices[0]["delta"]
                if "content" in delta:
                    response += delta["content"]
                    message_placeholder.markdown(response + "▌")
                else:
                    break
        message_placeholder.markdown(response)
    # 히스토리에 추가
    st.session_state.messages.append(
        {"role": "system", "content": response}
    )
