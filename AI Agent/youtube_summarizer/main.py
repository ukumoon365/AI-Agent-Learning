import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Models
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import urlparse
from langchain_community.document_loaders import YoutubeLoader

# Prompt
SUMMARIZE_PROMPT = """
다음 콘텐츠의 내용을 약 {selected_text_length}자 정도로 핵심 정리 및 알기 쉽게 요약 해주세요.
========
{content}
========
반드시 {selected_language}로만 작성해 주세요!
다른 언어로 요약하지마세요.
"""

ANSWER_PROMPT = """
{content} 내용에 대한 {user_input}에 대해 사실된 답변을 해주세요. 답변 전에 사실 검증 후 거짓없는 답변만 해주세요.  
"""

# Page Setting
def init_page():
    st.set_page_config(page_title="Yotute_Summarizer", page_icon="🔎")
    st.header("유튜브의 핵심 내용을 한눈에 🔎")
    st.sidebar.title("Options")

# Select Model
def select_model(temperature=0):
    models = ("gemini-3.5-flash-lite", "claude-haiku-5-5", "gpt-6-luna")
    selected_model = st.sidebar.radio("AI Models", models, key="Select Model")

    if selected_model == "gemini-3.5-flash-lite":
        st.session_state.model_name = "gemini-3.5-flash-lite"
        return ChatGoogleGenerativeAI(
            temperature = temperature,
            model = st.session_state.model_name
        )
    elif selected_model == "claude-haiku-5-5":
        st.session_state.model_name = "claude-haiku-5-5"
        return ChatAnthropic (
            temperature = temperature,
            model = st.session_state.model_name
        )
    elif selected_model == "gpt-6-luna":
        st.session_state.model_name = "gpt-6-luna"
        return ChatOpenAI(
            temperature = temperature,
            model = st.session_state.model_name
        )

# Select Language
def select_language():
    languages =("한국어", "日本語", "English")
    selected_language = st.sidebar.radio("Summary Language", languages, key="selete_language")
    return selected_language

# Select Text Length
def select_text_length():
    selected_text_length = st.sidebar.slider(
        "Text Length", min_value=100, max_value=1000, value=100, step=100
    )
    return selected_text_length

# Summarizer chain
def init_summarizer_chain(llm):
    prompt = ChatPromptTemplate.from_messages([("user", SUMMARIZE_PROMPT)])

    output_parser = StrOutputParser()

    return prompt | llm | output_parser    

# Answer chain
def init_answer_chain(llm):
    prompt = ChatPromptTemplate.from_messages([("user", ANSWER_PROMPT)])

    output_parser = StrOutputParser()

    return prompt | llm | output_parser

# Get Content
def get_content(url):
    # 영상의 자막 
    with st.spinner("Fetching Youtube ..."):
        try:
            # 자막 언어 선택
            if select_language == "日本語":
                selected_language = "jp"
            elif select_language == "English":
                selected_language = "en"
            else: selected_language = "ko"

            loader = YoutubeLoader.from_youtube_url(
                url, 
                add_video_info = False, # 불필요한 메타데이터 요청 제거
                language = [selected_language, "en"])
            res = loader.load()

            if res:
                return res[0].page_content
            else:
                return None
        except Exception as e:
            st.error(f"Error occurred: {e}")
            st.write(traceback.format_exc())
            return None

# URL Validate
def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Clear Chat
def clear_chat():
    clear_button = st.sidebar.button("대화 내역 삭제",key="clear")

    if clear_button or "message_history" not in st.session_state:
        st.session_state.message_history = []

def main():
    init_page()
    selected_language = select_language()
    selected_text_length = select_text_length()
    llm = select_model()
    summarizer_chain = init_summarizer_chain(llm)
    answer_chain = init_answer_chain(llm)
    clear_chat()

    if st.button("다시 요약하기"):
        st.session_state.previous_url = None


    if url := st.text_input("URL:",key="input"):
        if url != st.session_state.get("previous_url"):
            st.session_state.message_history = [] 
            is_valid_url = validate_url(url)
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