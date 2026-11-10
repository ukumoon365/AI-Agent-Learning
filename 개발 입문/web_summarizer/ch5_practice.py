import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# LLM 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# Prompt
SUMMARIZE_PROMPT = ""
# 페이지 설정 함수
def init_page():
    st.set_page_config(page_title="Web_Summarizer", page_icon="📝")
    st.header("Web_Summarizer Practice 📝")
    st.sidebar.title("Options")

# 모델 선택 함수
def select_model(temperature=0):
    models = ("gemini-3.5-flash-lite", "claude-haiku-5-5", "gpt-6-luna")
    selected_model = st.sidebar.radio("모델 선택", models, key="select_model")

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

# 체인 함수
def init_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_messages([("user", SUMMARIZE_PROMPT)])

    output_parser = StrOutputParser()

    return prompt | llm | output_parser    

def main():
    init_page()
    chain = init_chain()
    

if __name__ == "__main__":
    main()