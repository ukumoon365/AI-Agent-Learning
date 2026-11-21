"""
대문자 변환 함수 Lambda
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

prompt = PromptTemplate.from_template("Say: {content}")


# 대문자 변환 함수
def to_upper(x):
    return {"content": x["content"].upper()}


# RunnableLambda로 감싸서 chain에서 사용 가능하도록 만듬
to_upper = RunnableLambda(to_upper)
# Lambda식 사용 가능
# to_upper = RunnableLambda(lambda x: {"content": x["content"].upper()})

# chain에서 사용
to_upper_chain = to_upper | prompt

# 결과 출력
print(to_upper_chain.invoke({"content": "hello world"}))

"""
====================================================================================
모델 선택 Lambda
"""
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

openai_chain = ChatOpenAI(model = "gpt-6-luna")
goole_chain = GoogleGenerativeAI(model = "gemini-3.5-flash-lite")

def route_chain(query):
    if "Google" in query or "BigQuery" in query:
        return goole_chain
    else:
        return openai_chain

chain = RunnableLambda(route_chain)

print(chain.invoke("BigQuery에 대해 알려줘, 먼저 너의 모델 이름을 알려줘"))
# content='안녕하세요! 먼저 제 모델 이름은 **Gemini**입니다. 구글(Google)에서 개발한 인공지능 모델입니다.'

# print(chain.invoke("너의 모델 이름을 알려줘"))
# content='저는 OpenAI의 ChatGPT입니다. 정확한 모델명은 현재 제게 공개되어 있지 않습니다.'

"""
====================================================================================
.map() 사용한 내부 병렬 처리
"""
split = RunnableLambda(lambda x: x["content"].split(" ")) # 공백 구분으로 문자열 리스트화
to_upper = RunnableLambda(lambda x: x.upper()) # 대문자 변환
join = RunnableLambda(lambda x: " ".join(x)) # 문자 합치기

to_upper_chain = split | to_upper.map() | join
print(to_upper_chain.invoke({"content": "hi, hello world"}))
# HI, HELLO WORLD
