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

ANSWER_PROMPT = """
{content} 내용에 대한 {user_input}에 대해 사실된 답변을 해주세요. 답변 전에 사실 검증 후 거짓없는 답변만 해주세요.  
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
    selected_language = st.sidebar.radio("Summary Language", languages, key="selete_language")
    return selected_language

# 글자수 설정 함수
def select_text_length():
    selected_text_length = st.sidebar.slider(
        "Text Length", min_value=100, max_value=1000, value=100, step=100
    )
    return selected_text_length

# 내용 요약 체인 함수
def init_summarizer_chain(llm):
    prompt = ChatPromptTemplate.from_messages([("user", SUMMARIZE_PROMPT)])

    output_parser = StrOutputParser()

    return prompt | llm | output_parser    

# 질의응답 체인 함수
def init_answer_chain(llm):
    prompt = ChatPromptTemplate.from_messages([("user", ANSWER_PROMPT)])

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

# 대화 내역 삭제
def clear_chat():
    clear_button = st.sidebar.button("대화 내역 삭제",key="clear")

    # 대화 내역 리스트 추가
    if clear_button or "message_history" not in st.session_state:
        st.session_state.message_history = []

def main():
    init_page()
    selected_language = select_Language()
    selected_text_length = select_text_length()
    llm = select_model()
    summarizer_chain = init_summarizer_chain(llm)
    answer_chain = init_answer_chain(llm)
    clear_chat()
    if st.button("다시 요약하기"):
        st.session_state.previous_url = None
    # st.write("현재 선택된 언어:", selected_language) # 언어 변경 확인용


    # URL입력 시 요약 수행
    if url := st.text_input("URL:",key="input"):
        if url != st.session_state.get("previous_url"):
            st.session_state.message_history = [] # url 변경 시 대화 내역 초기화
            is_valid_url = validate_url(url)    # url 유효성 검사
            if not is_valid_url:
                st.write("잘못된 입력입니다. 다시 입력해주세요")
            else:
                if content := get_content(url):
                    st.session_state.summary = summarizer_chain.stream({
                        "content": content,
                        "selected_language": selected_language,
                        "selected_text_length": selected_text_length,
                        })

                    st.session_state.previous_url = url
                    st.session_state.content = content

    if "summary" in st.session_state:
        st.markdown("## 요약 내용")
        st.write(st.session_state.summary)

        st.markdown("-----------------")
        st.markdown("## 원본 내용")
        st.write(st.session_state.content)

                    
    # 해당 내용에 대한 질의응답 
    for msg in st.session_state.message_history:
         st.chat_message(msg["role"]).markdown(msg["response"])

    if user_input := st.chat_input("메세지를 입력하세요"):
        st.session_state.message_history.append(
            {"role": "user", "response": user_input})
        
        st.chat_message("user").markdown(user_input)

        with st.spinner("생각하는 중 ⏳"):
            with st.chat_message("assistant"):
                response = st.write_stream(
                    answer_chain.stream({
                        "content": st.session_state.content,
                        "user_input": user_input
                    })
                )
        st.session_state.message_history.append(
            {"role": "assistant", "response": response})

if __name__ == "__main__":
    main()