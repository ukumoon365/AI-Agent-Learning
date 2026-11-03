import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# 페이지 제목 및 아이콘 설정
st.set_page_config(page_title="Practice AI Chat", page_icon="📝")

# 페이지의 헤더 설정
st.header("Practice AI Chat for Google AI 📝")

# LLM 모델 설정
llm = GoogleGenerativeAI(model = "gemini-3.1-flash-lite", temperature=0)
# model = "" -> 모델 버전 설정
# temperature = 0~1 -> 생성되는 텍스트의 무작위성 / 다양성 조절 -> 상황과 목적에 맞는 값으로 설정 
# 값이 클 수록 무작위성이 높아져 다양한 응답 기대 가능 / 관련성 낮는 응답 가능성 존재
# 예측 가능 및 일관성 있는 응답 기대 가능 / 다양성은 낮아짐
# temperature=2로 설정 시 고장 초래 가능성 존재

# 프롬로트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 불친절하고 진상의 아저씨입니다"),
    ("user","{input}")
])
# 출력 파서
output_parser = StrOutputParser()

# 프롬포트 -> 모델 -> 출력 파서를 하나의 chain으로 연결 (파이프라인 사용)
# 입력부터 출력까지 과정을 선언형으로 구성
chain = prompt | llm | output_parser

# 입력창 구현
if user_input := st.chat_input("궁금한 것을 입력해주세요."):
    # invoke()로 chain 실행 -> LLM에서 질문 전달
    response = chain.invoke({"input": user_input})

    # 응답 출력
    print(response)



# 다른 방법의 입력창 구현
# container = st.container() # 여러 위젯을 모아 보여줄 영역 설정

# with container:
      # 사용자의 입력값을 한 번에 제출 / Submit 버튼이 눌리기 전까지는 실행 X
#     with st.form(key='my_form', clear_on_submit=True):
#         user_input = st.text_area(label='Message: ', height=100) # 여러 줄의 텍스트 입력 가능 영역 설정
#         submit_button = st.form_submit_button(label='Send') # 전송 버튼 생성

#     if submit_button and user_input:
#         print("yes")
