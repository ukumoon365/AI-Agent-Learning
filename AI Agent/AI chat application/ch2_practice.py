import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
load_dotenv()

def Ai_chat():
    # 페이지 제목 및 아이콘 설정
    st.set_page_config(page_title="Practice AI Chat", page_icon="📝")

    # 페이지의 헤더 설정
    st.header("Practice AI Chat for Google AI 📝")

    # LLM 모델 설정
    llm = GoogleGenerativeAI(model = "gemini-3.1-flash-lite", temperature=0)

    # 프롬로트 템플릿 생성
    prompt = ChatPromptTemplate.from_messages([
        ("system", "친절한 AI Agent, 답변 전에 사실확인, 검증하고 답변할 것"), # 프롬포트 작성
        ("user","{input}") # 입력값 전달
    ])
    # LLM 응답을 텍스트로 변환하는 파서
    output_parser = StrOutputParser()

    # 프롬포트 -> 모델 -> 출력 파서를 하나의 chain으로 연결 (파이프라인 사용)
    # 입력부터 출력까지 과정을 선언형으로 구성
    chain = prompt | llm | output_parser

    # 채팅 이력 초기화 / history가 없다면 새로 생성
    if "message_history" not in st.session_state:
        # history 생성
        st.session_state.message_history = []

    # 입력창 / 사용자 입력 감시
    if user_input := st.chat_input("궁금한 것을 입력해주세요."):
        # 로딩화면 출력
        with st.spinner("잠시만 기다려주세요"):
        # invoke()로 chain 실행 -> LLM에서 질문 전달
            response = chain.invoke({
                "history": st.session_state.message_history, # 대화 이력 전달
                "input": user_input # 입력값 전달
            })
        # 이력에 입력 내용 추가
        st.session_state.message_history.append(("user", user_input))
        # 이력에 답변 내용 추가
        st.session_state.message_history.append(("assistant", response))

        # UI에 과거 대화 표시
        for role, message in st.session_state.get("message_history", []):
            # 채팅 메세지 영역 생성
            with st.chat_message(role):
                # 영역 안에 메세지 출력
                st.markdown(message)

if __name__ == "__main__":
    Ai_chat()