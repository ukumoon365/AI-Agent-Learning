from langchain_core.runnables import ConfigurableField
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI

test_model = GoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0,
).configurable_fields(
    model=ConfigurableField(
    id="model", # 식별자 ( 설정을 구분하는 용도)
    name="Model Name", # 설정 항목을 설명
    description="The model name of the LLM", # 설명
    )
)
test_model = test_model.with_config(configurable={"model": "gemini-3.6-flash"})

# 모델 변경 알고리즘
test_model = ChatOpenAI(temperature=0).configurable_alternatives(
    ConfigurableField(id="model"), 
    default_key="openai", # 기본값 openai
    google=GoogleGenerativeAI(temperature=0, modle="gemini-2.5-flash")
    )

test_model.with_config(configurable={"model": "google"}) # 모델 gemini로 변경