# Chapter 3 Practice
```text
✔️ Sidebar
    - sidebar UI추가
    st.sidebar.title(""): 사이드바 제목 설정

✔️ slider
    - 슬라이드 조절 옵션 추가
    st.sidebar.slider("제목", min_value=값, max_value=값, value=값, step=값)
temperature = st.sidebar.slider(
                "답변 다양성", min_value=0.0, max_value=2.0, value= 0.0, step= 0.1)
✔️ button
        ○ 버튼을 생성하고 클릭 여부를 확인
        ✅ st.button은 bloon형 -> 기본 False / 버튼 눌림 True
    st.sidebar.button("제목", key="고유식별 ID")
clear_button = st.sidebar.button("대화 내역 삭제",key="clear")
    
✔️ radio
        ○ 여러 선택지 중 하나 선택
        ✅st.radio는 해당 값을 반환
    st.sidebar.radio("제목", 값들, key="고유식별ID")
select_model = st.sidebar.radio("모델 선택",models, key="selected_model")


✔️ markdown에 f-string
st.sidebar.markdown(f"- Input cost: ${cost_input:.2f}")

✔️ LCEL (LangChain Expression Language) 기초
    LangChain의 구성 요소(Prompt, LLM, Output Parser 등)를 연결하여 AI 애플리케이션의 실행 흐름(Chain)을 간결하게 구성
    - invoke
    체인 전체를 순차적으로 실행 함수
    
    - batch
    여러 개의 입력을 한번에 처리 
    chain, batch -> 병렬처리
    ✅ 대용량 데이터 / 여러 처리를 동시에 처리할 때 전체 처리 시간을 단축 가능
        ○ config의 max_concurrency 옵션으로 동시 요청 개수 제한 가능
        ✅ Rate Limit error 발생시 max_concurrency 값을 낮추면 해결 가능
        
    - streaming
    LLM에서 생성된 토큰을 순차적 전달 (토큰 단위)
    
    ✔️ 동기 / 비동기
        ○ 동기 (기존 방식)
        하나의 작업이 완료될 때까지 기다린 후 다음 작업을 실행
        ✅ 작업이 완료된 후 다음 작업을 진행해야 하거나, 다른 작업을 동시에 진행할 필요가 없는 경우에 적합
    
        ○ 비동기
        하나의 작업이 완료될 때까지 기다리는 동안 다른 작업을 진행할 수 있는 실행
        ✅ 작업 대기 시간 효율적 사용
        ⚠️ 반드시 실행 시간이 단축되는 것은 ❌
            	동기(Synchronous)	    비동기(Asynchronous)
    실행 방식	작업 완료 후 다음 작업     작업 대기 중 다른 작업
    작업 대기	해당 흐름이 대기	        다른 작업에 실행 기회 제공
    특징	        순차적인 작업 처리	        대기 시간 활용에 효율적
    
        ✅ 최종 결과는 일반적 동일 / 실행 흐름, 반환 시점의 차이
        ✅ API 호출처럼 응답을 기다리는 시간이 길고, 그동안 다른 작업을 진행할 수 있는 경우에 적합
    
    LCEL	    동기 메서드	비동기 메서드
    단일 요청	invoke()	ainvoke()
    다중 요청	batch()	    abatch()
    순차 출력	stream()	astream()
    
    ✔️ 기타 기능
    - ConfigurableField 활용
    설정 항목을 미리 정의 가능
        ○ .configurable_fields로 정의
        ○ .with_config(configurable = { : })로 수정
from langchain_core.runnables import ConfigurableField
test_model = gemini(
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

        ○ 모델 변경 configurableField 활용
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

test_model = ChatOpenAI(temperature=0).configurable_alternatives(
    ConfigurableField(id="model"), 
    default_key="openai", # 기본값 openai
    google=GoogleGenerativeAI(temperature=0, modle="gemini-2.5-flash"))
test_model.with_config(configurable={"model": "google"}) # 모델 gemini로 변경

✅ 비슷한 처리를 여러 방식으로 분기해야 할 때 사용 고려

    - Fallback
    하나의 처리가 실패했을 때 다른 처리로 전환 기능
        ○ .with_fallback으로 설정
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI

prompt = PromptTemplate.from_template("이 주제로 농담을 해주세요: {topic}")
chain = prompt | ChatOpenAI(temperature=0)
google_chain = prompt | GoogleGenerativeAI(temperature=0, model="gemini-3.5-flash-lite")
fallback_chain = chain.with_fallbacks([google_chain]) # openai가 미응답시 gemini로 fallback
print(fallback_chain.invoke({"topic": "겨울"}))

    - RunnableParallel
    여러 개의 chain 병렬 실행
        ○ RunnableParallel로 설정
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel

prompt = PromptTemplate.from_template("이 주제로 농담을 해주세요: {topic}")
openai_chain = prompt | ChatOpenAI(temperature=0)
google_chain = prompt | GoogleGenerativeAI(temperature=0, model="gemini-3.5-flash-lite")
test_chain = RunnableParallel(openai=openai_chain, goole=google_chain) print(test_chain.invoke({"topic": "겨울"}))

        ○ RunnablePassthrough
        입력값을 다음 단계로 그대로 전달 or 넘기기 전에 임의의 처리 추가
        ○ RunnablelLambda : 임의의 함수를 chain에 포함
        ○ RunnableBranch: chain내에서 조긴 분기

✔️ Streamlit 스트리밍 출력
    - st.write_stream(): LLM 응답을 스트리밍 방식으로 출력
with st.chat_message("assistant"):
            response = st.write_stream(
                chain.stream(
                    {"history": st.session_state.message_history,
                        "user_input": user_input,})
)
    - 스트리밍 출력 흐름
    1) 과거 채팅 이력 표시 2) 스트리밍 출력으로 응답 출력 3) 채팅 이력에 응답 추가
for msg in st.session_state.message_history: # 과거 채팅 이력 표시
    st.chat_message(msg["role"]).markdown(msg["content"])
if user_input := st.chat_input("궁금한 내용을 입력해주세요."): # 사용자 입력 모니터링
    st.session_state.message_history.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    with st.chat_message("assistant"): # LLM응답 스트리밍 출력
                response = st.write_stream(
                    chain.stream(
                        {"history": st.session_state.message_history,
                            "user_input": user_input,})
)
        st.session_state.message_history.append( # 채팅 이력 추가
            {"role": "assistant", "content": response})

 ✔️ 모델 변경 기능
temperature = st.sidebar.slider( # 모델 temperature 설정 변경 사이드 슬라이드바 추가
        "Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1
    )
    models = ("GPT-5 mini", "GPT-5", "Claude Sonnet 4.5", "Gemini 2.5 Flash")
    model = st.sidebar.radio("Choose a model:", models) # 모델 변경 사이드바 추가
    
    # 모델 변경 알고리즘
    if model == "GPT-5 mini":
        st.session_state.model_name = "gpt-5-mini"
        return ChatOpenAI(
            temperature=temperature,
            model=st.session_state.model_name,
        )
    elif model == "GPT-5":
        st.session_state.model_name = "gpt-5"
        return ChatOpenAI(
            temperature=temperature,
            model=st.session_state.model_name,
        )
    elif model == "Claude Sonnet 4.5":
        st.session_state.model_name = "claude-sonnet-4-5-20250929"
        return ChatAnthropic(
            temperature=temperature,
            model=st.session_state.model_name,
        )
    elif model == "Gemini 2.5 Flash":
        st.session_state.model_name = "gemini-2.5-flash"
        return ChatGoogleGenerativeAI(
            temperature=temperature,
            model=st.session_state.model_name,
        )

✔️ API 호출 비용 파악 및 출력
def calc_and_display_costs(): # 호출 비용 계산 함수
    output_count = 0
    input_count = 0

    for msg in st.session_state.message_history:
        token_count = get_message_counts(msg["content"])

        if msg["role"] == "assistant":
            output_count += token_count
        else:
            input_count += token_count

    if not st.session_state.message_history:
        return # 함수 종료 용도
    
    # 비용 계산
    cost_input = MODEL_PRICES["input"][st.session_state.model_name] * input_count
    cost_output = MODEL_PRICES["output"][st.session_state.model_name] * output_count
    cost = cost_input + cost_output

    # 호출 비용 사이드바 추가
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${cost:.5f}**")
    st.sidebar.markdown(f"- Input cost: ${cost_input:.5f}")
    st.sidebar.markdown(f"- Output cost: ${cost_output:.5f}")
```
