from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI

prompt = PromptTemplate.from_template("이 주제로 농담을 해주세요: {topic}")
chain = prompt | ChatOpenAI(temperature=0)
google_chain = prompt | GoogleGenerativeAI(temperature=0, model="gemini-3.5-flash-lite")
fallback_chain = chain.with_fallbacks([google_chain]) # openai가 미응답시 gemini로 fallback
fallback_chain.invoke({"topic": "겨울"})


