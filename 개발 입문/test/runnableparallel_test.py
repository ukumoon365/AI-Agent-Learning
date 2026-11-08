from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel

prompt = PromptTemplate.from_template("이 주제로 농담을 해주세요: {topic}")
openai_chain = prompt | ChatOpenAI(temperature=0)
google_chain = prompt | GoogleGenerativeAI(temperature=0, model="gemini-3.5-flash-lite")
test_chain = RunnableParallel(openai=openai_chain, goole=google_chain) 
test_chain.invoke({"topic": "겨울"})