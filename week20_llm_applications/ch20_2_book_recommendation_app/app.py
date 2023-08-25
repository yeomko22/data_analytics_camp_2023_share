from datetime import datetime, timezone
from typing import List, Generator

import openai
import pinecone
import streamlit as st
from google.cloud import translate
from google.oauth2.service_account import Credentials
from openai.openai_object import OpenAIObject

st.set_page_config(
    page_title="worms book",
    page_icon="📖",
)


@st.cache_resource
def init_google_translation_connection():
    credentials = Credentials.from_service_account_info(st.secrets.GOOGLE)
    return translate.TranslationServiceClient(credentials=credentials)


@st.cache_resource
def init_pinecone_connection():
    pinecone.init(
        api_key=st.secrets["PINECONE_KEY"],
        environment=st.secrets["PINECONE_REGION"]
    )
    index = pinecone.Index('bookstore')
    return index


def get_embedding(query):
    response = openai.Embedding.create(input=[query], model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


def get_translation(query):
    parent = f"projects/{st.secrets.PROJECTID}/locations/global"
    response = google_translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "mime_type": "text/plain",
            "source_language_code": "ko",
            "target_language_code": "en-US",
        }
    )
    translations = response.translations
    return translations[0].translated_text


google_translate_client = init_google_translation_connection()
pinecone_index = init_pinecone_connection()
openai.api_key = st.secrets.OPENAI_TOKEN
openai_model_version = "gpt-3.5-turbo-0613"

st.title("웜즈의 책방 📖🐛")
st.image("./images/banner.png")


def recommend(query_embedding):
    results = pinecone_index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True,
    )
    matches = results["matches"]
    return [x["metadata"] for x in matches]


def generate_prompt(query):
    prompt = f"""
유저가 읽고 싶은 책에 대한 묘사와 이에 대한 추천 결과가 주어집니다.
유저의 입력과 각 추천 결과 책의 제목, 저자, 소개 등을 참고하여 추천사를 작성하세요.
당신에 대한 소개를 먼저 하고, 친절한 말투로 작성해주세요.
중간 중간 이모지를 적절히 사용해주세요.

---
유저 입력: {query}

추천 결과 1
제목: {items[0]['title']}
저자: {items[0]['authors']}
책소개: {items[0]['summary']}

추천 결과 2
제목: {items[1]['title']}
저자: {items[1]['authors']}
책소개: {items[1]['summary']}

추천 결과 3
제목: {items[2]['title']}
저자: {items[2]['authors']}
책소개: {items[2]['summary']}
---
"""
    return prompt


def request_chat_completion(prompt):
    response = openai.ChatCompletion.create(
        model=openai_model_version,
        messages=[
            {"role": "system", "content": "당신은 책을 추천해주는 책방지기, 웜즈입니다."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    return response


def get_author_title(item):
    author = item["authors"]
    title = item["title"]
    author_list = author.split(",")
    if len(author_list) > 1:
        author = f"{author_list[0]} 외 {len(author_list) - 1}인"
    return f"{author} - {title}"


def process_recommend_results(items):
    st.markdown("**추천결과 🎁 (열 수 있어요!)**")
    for i, item in enumerate(items):
        with st.expander(f"#{i+1} {get_author_title(item)}"):
            st.header(item["title"])
            st.write(f"**{item['authors']}** | {item['publisher']} | {item['published_at']} | [yes24]({item['url']})")
            col1, col2 = st.columns([0.25, 0.75], gap="medium")
            with col1:
                st.image(item["img_url"])
            with col2:
                st.write(item["summary"])


def process_generated_text(streaming_resp: Generator[OpenAIObject, None, None]) -> str:
    st.markdown("**웜즈의 추천사 ✍️**")
    report = []
    res_box = st.empty()
    for resp in streaming_resp:
        delta = resp.choices[0]["delta"]
        if "content" in delta:
            report.append(delta["content"])
            res_box.markdown("".join(report).strip())
        else:
            break
    result = "".join(report).strip()
    return result


with st.form("form"):
    query = st.text_input(
        label="읽고 싶은 책을 묘사하면 AI가 추천해줍니다💡",
        placeholder="ex) 좀비와 가족애를 다룬 이야기"
    )
    submitted = st.form_submit_button("제출")
if submitted:
    if not query:
        st.error("읽고 싶은 책 묘사를 작성해주세요")
    else:
        with st.spinner("웜즈가 책을 찾고 있습니다..."):
            translated_query = get_translation(query)
            query_embedding = get_embedding(translated_query)
            items = recommend(query_embedding)
        process_recommend_results(items)

        with st.spinner("웜즈가 추천사를 작성합니다..."):
            prompt = generate_prompt(query, items)
            streaming_resp = request_chat_completion(prompt)
        process_generated_text(streaming_resp)
