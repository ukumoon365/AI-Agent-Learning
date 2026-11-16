import traceback # 오류 발생 위치, 호출 과정 추적 모듈
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter # 텍스트 분할 도구
from langchain_core.runnables import RunnableLambda # Runnable 객체로 변환하는 클래스
import tiktoken
# LLM 
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
# 웹페이지 관련 패키지
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def select_model(temperature = 0): # 제미나이로 지정
    selected_model = "gemini-3.5-flash-lite"
    return ChatGoogleGenerativeAI(
            temperature = temperature,
            model=selected_model)

def init_summarize_chain(llm):
    prompt = ChatPromptTemplate.from_messages(["다음 콘텐츠의 내용을 약 300자 정도로 핵심 정리 및 알기 쉽게 요약 해주세요 {content}"])

    output_parser = StrOutputParser()
    return prompt | llm | output_parser

def init_chain(summarize_chain):
    # 텍스트 분할
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-5", # tiktoken 토큰 계산에 사용할 모델 지정 / 제미나이는 tiktoken 지원 X -> gpt로 대체
        chunk_size=16000, # 하나의 청크에 포함할 최대 토큰 수
        chunk_overlap = 0, # 요약에는 중복 불필요
    )

    text_split = RunnableLambda(
        lambda x: [{"content": doc} for doc in text_splitter.split_text(x["content"])] 
    )

    text_concat = RunnableLambda(lambda x: {"content": "\n".join(x)})

    map_reduce_chain = (
        text_split | summarize_chain.map() | text_concat | summarize_chain
    )

    def route(x):
        encoding = tiktoken.encoding_for_model("gpt-5")
        token_count = len(encoding.encode(x["content"]))

        if token_count > 16000:
            return map_reduce_chain
        else:
            return summarize_chain

    chain = RunnableLambda(route)
    return chain

# 웹페이지 불러오기 함수
def get_content(url):
    try:    # 오류 방지 try
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
        print("Error")

# URL 유효성 검사 함수
def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

if __name__ == "__main__":
    url = input()
    llm = select_model()
    summarize_chain = init_summarize_chain(llm)
    chain = init_chain(summarize_chain)

    if content := get_content(url):
        print(chain.invoke({"content": content}))