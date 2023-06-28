import streamlit as st
import openai

st.title("AI Copywriter✍️")
openai.api_key = st.secrets.OPENAI_TOKEN


def generate_prompt(name, description, keywords, n):
    prompt = f"""
특정 제품 혹은 브랜드를 광고하기 위한 문구를 {n}개 생성해주세요.
제품의 특징이 드러나야 합니다.
키워드가 주어질 경우, 반드시 키워드 중 하나를 포함해야 합니다.
초등학생의 말투로 작성해주세요.
이모지를 하나 이상 포함해 주세요.

---
제품/브랜드 이름: {name}
제품 간단 정보: {description}
키워드: {keywords}
---
"""
    return prompt.strip()


def request_chat_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 프로 카피라이터입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]


with st.form("my_form"):
    name = st.text_input("제품/브랜드 이름(필수)", placeholder="카누")
    desc = st.text_input("제품 간단 정보(필수)", placeholder="브라질 원두로 깊은 풍미")
    st.text("포함할 키워드(최대 3개까지 허용)")

    col1, col2, col3 = st.columns(3)
    with col1:
        keyword_one = st.text_input(
            placeholder="키워드 1",
            label="keyword_one",
            label_visibility="collapsed"
        )
    with col2:
        keyword_two = st.text_input(
            placeholder="키워드 2",
            label="keyword_two",
            label_visibility="collapsed"
        )
    with col3:
        keyword_three = st.text_input(
            placeholder="키워드 3",
            label="keyword_three",
            label_visibility="collapsed"
        )

    submitted = st.form_submit_button("Submit")
    if submitted:
        if not name:
            st.error("제품/브랜드 이름을 입력해주세요.")
        elif not desc:
            st.error("제품 간단 설명을 입력해주세요.")
        else:
            keywords = [keyword_one, keyword_two, keyword_three]
            keywords = [x for x in keywords if x]
            prompt = generate_prompt(name, desc, keywords, n=3)
            with st.spinner("AI 카피라이터가 광고 문구를 생성 중입니다..."):
                generated_text = request_chat_completion(prompt)
                st.text_area(
                    label="마케팅 문구 생성 결과",
                    value=generated_text,
                    height=200
                )
