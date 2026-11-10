import traceback # 오류 발생 위치, 호출 과정 추적 모듈
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# LLM 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
# 웹페이지 관련 패키지
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# Prompt
SUMMARIZE_PROMPT = """
다음 콘텐츠의 내용을 약 {selected_text_length}자 정도로 핵심 정리 및 알기 쉽게 요약 해주세요.
========
{content}
========
{selected_language}로 작성해 주세요!
"""
# 페이지 설정 함수
def init_page():
    st.set_page_config(page_title="Web_Summarizer", page_icon="🔍")
    st.header("웹페이지의 핵심 내용을 한눈에 🔍")
    st.sidebar.title("Options")

# 모델 선택 함수
def select_model(temperature=0):
    models = ("gemini-3.5-flash-lite", "claude-haiku-5-5", "gpt-6-luna")
    selected_model = st.sidebar.radio("AI Models", models, key="select_model")

    if selected_model == "gemini-3.5-flash-lite":
        st.session_state.model_name = "gemini-3.5-flash-lite"
        return ChatGoogleGenerativeAI(
            temperature = temperature, 
            model = st.session_state.model_name)
    elif selected_model == "claude-haiku-5-5":
        st.session_state.model_name = "claude-haiku-5-5"
        return ChatAnthropic(
            temperature = temperature, 
            model = st.session_state.model_name)
    elif selected_model == "gpt-6-luna":
        st.session_state.model_name = "gpt-6-luna"
        return ChatOpenAI(
            temperature = temperature, 
            model = st.session_state.model_name)

# 요약 언어 설정 함수
def select_Language():
    languages =("한국어", "日本語", "English")
    selected_language = st.sidebar.radio("Languages", languages, key="selete_language")
    return selected_language

# 글자수 설정 함수
def select_text_length():
    selected_text_length = st.sidebar.slider(
        "Text Length", min_value=100, max_value=1000, value=100, step=100
    )
    return selected_text_length

# 체인 함수
def init_chain():
    llm = select_model()
    
    prompt = ChatPromptTemplate.from_messages([("user", SUMMARIZE_PROMPT)])

    output_parser = StrOutputParser()

    return prompt | llm | output_parser    

# 웹페이지 불러오기 함수
def get_content(url):
    try:    # 오류 방지 try
        with st.spinner("웹페이지 읽는 중 ⏳"):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # 본문일 가능성이 높은 요소 채택
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            else:
                return soup.body.get_text()
    except: # 오류 발생 시
        st.write(traceback.format_exc())

# URL 유효성 검사 함수
def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def main():
    init_page()
    selected_language = select_Language()
    selected_text_length = select_text_length()
    chain = init_chain()

    # URL입력 시 요약 수행
    if url := st.text_input("URL:",key="input"):
        is_valid_url = validate_url(url)    # url 유효성 검사
        if not is_valid_url:
            st.write("잘못된 입력입니다. 다시 입력해주세요")
        else:
            if content := get_content(url):
                st.markdown("## 요약 내용")
                st.write_stream(chain.stream({
                    "content": content,
                    "selected_language": selected_language,
                    "selected_text_length": selected_text_length,
                    }))
                st.markdown("-----------------")
                st.markdown("## 원본 내용")
                st.write(content)


if __name__ == "__main__":
    main()