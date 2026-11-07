# Chapter 2 Practice
```text
Streamlit
⭐ 사용자의 입력과 조작에 반응하여 동적으로 다시 실행하는 방식으로 동작

✔️ 필요한 라이브러리 및 모듈 import"
    - streamlit (웹페이지 제작)
import streamlit as st 
    - langchain (LLM 호출 용도 사용)
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
    - dotenv (API 저장 용도 사용)
from dotenv import load_dotenv
load_dotenv()

✔️ 화면 요소 배치
    - 페이지 제목 및 아이콘 설정
        ○ st.set_page_config()
        웹페이지의 기본 정보를 설정하는 함수
            st.set_page_config(page_title=" ", page_icon=" ")
            
    - 페이지 헤더 설정
        ○ st.header()
        페이지 헤더(큰 제목) 설정 함수
            st.header(" ")

    - UI요소를 묶어 배치 
        ○ st.contaner()
        여러 위젯을 모아 보여주는 영역 생성 함수
        1) 영역 변수 초기화
            container = st.container()
        2) 컨테이너 함수 설정
            § st.form()
            사용자의 입력값을 한번에 제출 할 수 있는 입력 양식 생성 
                ✅ form내부의 위젯은 Submit 버튼이 눌리기 전 까지는 실행 ❌
            with st.form(key='my_form', clear_on_submit=True):
            § st.text_area
            여러 줄의 텍스트를 입력할 수 있는 영역 생성
            user_input = st.text_area(label='Message: ', height=100)
            § st.form_submit_button()
            form의 내용을 전송하는 버튼 생성
            submit_button = st.form_submit_button(label='Send')
            § 그 외
                □ st.slider(): 슬라이더 생성
                □ st.selectbox(): 드롭다운 메뉴 생성
                □ st.image(): 이미지 표시 
                ....
        3) 내용 입력 & Submit 버튼 눌림 후 작동
        if submit_button and user_input:
    
        

✔️ LLM 모델 설정
    - 버전, 텍스트 무작위성 설정
    llm = GoogleGenerativeAI(model = "모델 버전", temperature=0)
    ✅ temperature 
        ○ 생성되는 텍스트의 무작위성 (다양성) 설정
        값이 클 수록 무작위성 ⬆️ -> ⚠️ 관련성 낮은 응답 가능성 존재
        값이 작을 수록 무작위성 ⬇️ -> 예측 가능, 일관성 있는 답변 / (⚠️ 답변의 다양성 ⬇️)
        범위는 0~1 권장 / ⚠️ 2 이상 설정 시 고장 초래 가능성 존재
        ➡️ 상황과 목적에 맞는 값 설정 필요
        
    - 프롬포트 템플릿
    prompt = ChatPromptTemplate.from_messages([
        ("system", "프롬포트 내용"),
        ("user","{input}") 
        ])
        
        ○ System Message
        LLM의 답변 방식, 행동 원칙을 결정하는 기본적인 지시
            § 답변의 톤, 스타일 지정
            § 규칙 및 제약 조건 
            § 수행할 역할 지정
            § 우선시 할 관점, 기준 
            ....
    
    - LLM 응답을 텍스트로 변환
    output_parser = StrOutputParser()
        ○ 입력값을 텍스트로 변환하는 파서
        
    - 사용자의 입력값을 LLM에 전달하는 체인
    chain = prompt | llm | output_parser
    | (파이프 라인)을 이용하여 결과 값을 오른쪽으로 전달
            § 프롬프토을 LLM에 전달 -> LLM의 답변을 아웃풋 파서에 전달 
    
✔️ 사용자 입력 처리
    ✅ st.session_state
        애플리케이션의 상태 관리를 하기 위한 기능 (데이터 공유, 사용자의 상호 작용에 따른 정보 유지)
        ○ DIct / list 형식으로 저장
            리스트 []: 대화 메시지를 순서대로 보관
            딕셔너리 {}: 개별 메시지의 역할과 내용 저장
        ○ 사용자 마다 독립적인 session_state 생성
        
    ⚠️ 대부분의 LLM은 stateless 구조 (상태 기억 ❌) 
        ➡️ session_state에 message_history라는 key에 채팅 이력 저장
    
    1) 채팅 이력 초기화(생성) 
        if "message_history" not in st.session_state:
        st.session_state.message_history = []
    2) 사용자 입력 감시 및 입력 처리
        1) 입력값 입력
        if user_input := st.chat_input(" "):
            ✅ := (walrus Operator): 변수 값 할당과 동시 조건문에 사용 연산자
        
        2) 로딩 표시 기능
            § st.spinner()
            Streamlit에서 작업 진행 중 로딩 표시 기능 함수
        with st.spinner(" "):
        ✅ with: 작업의 시작과 종료를 수행
                spinner (로딩 표시)를 시작 밑의 실행 코드 작업이 끝나면 종료 (로딩 표시 종료)
        
        3) 입력값을 chain을 통해 LLM에 전달 
        chain: prompt (입력값) -> LLM -> parser (텍스트 변환)
            response = chain.invoke({
                "history": st.session_state.message_history, # 대화 이력
                "input": user_input # 입력값
            }
        4) 채팅 내역 저장
        st.session_state.message_history.append(("user", user_input)) # 입력값
        st.session_state.message_history.append(("assistant", response)) # 답변
✔️ 대화 이력 UI에 표시
        for role, message in st.session_state.get("message_history", []):
            § st.chat_message(): 채팅 메세지 표시 영역 생성
            with st.chat_message(role):
            § st.markdown(): 생성된 영역 안에 메세지 출력
                st.markdown(message)
```