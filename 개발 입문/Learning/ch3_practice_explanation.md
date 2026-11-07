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
        id="model",
        name="Model Name",
        description="The model name of the LLM",
    )
)
test_model = test_model.with_config(configurable={"model": "gemini-3.6-flash"})
```
