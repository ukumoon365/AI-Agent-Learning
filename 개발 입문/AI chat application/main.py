import tiktoken
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI as gemini # gemini-3.5-flash-lite
from langchain_anthropic import ChatAnthropic as claude # claude-haiku-5-5
from langchain_openai import ChatOpenAI as gpt # gpt-6-luna
load_dotenv()

# 2026 11월 기준 모델 가격 
MODEL_PRICES = {
    "input": {
        "gemini-3.5-flash-lite": 0.30 / 1_000_000,
        "claude-haiku-5-5": 0.1 / 1_000_000,
        "gpt-6-luna": 0.10 / 1_000_000,
    },
    "output": {
        "gemini-3.5-flash-lite": 2.50 / 1_000_000,
        "claude-haiku-5-5": 0.50 / 1_000_000,
        "gpt-6-luna": 0.50 / 1_000_000,
    },
}

def page_settings():
    model_name = st.session_state.get(
        "selected_model", "gemini-3.5-flash-lite")
    st.set_page_config(page_title="Practice AI Chat", page_icon="💬")
    st.header(f"반갑습니다 연습용 AI Chat📝 - \n + {model_name}")
    st.sidebar.title("Options")


def model_settings():
    # temperature 설정 (0.0 ~ 2.0) 
    temperature = st.sidebar.slider(
        "답변 다양성", min_value=0.0, max_value=2.0, value= 0.0, step= 0.1)

    models = ("gemini-3.5-flash-lite", "claude-haiku-5-5", "gpt-6-luna")
    select_model = st.sidebar.radio("모델 선택",models, key="selected_model")

    if select_model == "gpt-6-luna":
        st.session_state.model_name = "gpt-6-luna"
        return gpt(
            temperature = temperature,
            model=st.session_state.model_name
        )
    elif select_model == "claude-haiku-5-5":
        st.session_state.model_name = "claude-haiku-5-5"
        return claude(
            temperature=temperature,
            model=st.session_state.model_name
        )
    elif select_model == "gemini-3.5-flash-lite":
        st.session_state.model_name = "gemini-3.5-flash-lite"
        return gemini(
            temperature=temperature,
            model=st.session_state.model_name
        )

def init_chain():
    # LLM 모델 설정 함수 호출 및 저장
    st.session_state.llm = model_settings()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI Agent입니다."),
        ("user","{input}")
    ])

    output_parser = StrOutputParser()
    return prompt | st.session_state.llm | output_parser

def clear_chat():
    clear_button = st.sidebar.button("대화 내역 삭제",key="clear")

    if clear_button or "message_history" not in st.session_state:
        st.session_state.message_history = []

def get_message_counts(text):
    if "gemini" in st.session_state.model_name:
        return st.session_state.llm.get_num_tokens(text)
    else:
        if "gpt" in st.session_state.model_name:
            encoding = tiktoken.encoding_for_model(st.session_state.model_name)
        else:
            encoding = tiktoken.encoding_for_model("gpt-4o") # claude는 토크나이저 미제공
        return len(encoding.encode(text))

def display_costs():
    output_count = 0
    input_count = 0

    for msg in st.session_state.message_history:
        token_count = get_message_counts(msg["response"])
        if msg["role"] == "assistant":
            output_count += token_count
        else:
            input_count += token_count

    if not st.session_state.message_history:
        return
        
    model_name = st.session_state.model_name
    cost_input = MODEL_PRICES["input"][model_name] * input_count
    cost_output = MODEL_PRICES["output"][model_name] * output_count

    total_cost = cost_input + cost_output

    # 코스트 표시
    st.sidebar.markdown("## 비용")
    st.sidebar.markdown("**비용 계산**")
    st.sidebar.markdown(f"- Input cost: ${cost_input:.2f}")
    st.sidebar.markdown(f"- Output cost: ${cost_output:.2f}")
    st.sidebar.markdown(f"- total cost: ${total_cost:.2f}")

def Ai_chat():
    # 페이지 설정
    page_settings()
    # LLM 모델 설정
    chain = init_chain()
    # 채팅 설정
    clear_chat()

    # UI출력
    for msg in st.session_state.message_history:
        st.chat_message(msg["role"]).markdown(msg["response"])

    if user_input := st.chat_input("메세지를 입력하세요"):
        st.session_state.message_history.append(
            {"role": "user", "response": user_input})
        
        st.chat_message("user").markdown(user_input)

        with st.spinner("답을 찾는 중 ⏳"):
            with st.chat_message("assistant"):
                response = st.write_stream(
                                chain.stream({
                                "history": st.session_state.message_history,
                                "input": user_input
                                })
                            )
        st.session_state.message_history.append(
            {"role": "assistant", "response": response})
        
    # 비용 계산 표시
    display_costs()

if __name__ == "__main__":
    Ai_chat()
