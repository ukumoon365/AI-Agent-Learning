# Preparation & Understanding
```text
1) Open AI 준비
    1. 가상환경 생성 및 활성화
    2. LLM의 API 발급
    3. 환경변수 등록
        window: $env:이름 = "API 주소"
        linux: export 이름 = "API 주소"
    4. 각 라이브러리 설치
        python -m pip install --upgrade pip (pip 업데이트)
        python -m pip index versions 패키지 (설치 가능한 최신 버전 확인)
        python -m pip install openai (gpt 라이브러리)
        python -m pip install anthropic   (claude 라이브러리)
        python -m pip  install google-ai-generativelanguage (gemini 라이브러리)
        
✔️ 사용할 모델
    - OSS 모델
    오픈 소스 모델
    
    1. 질의 응답 모델
        일반적 LLM
        
    2. Embedding 모델
    텍스트의 의미를 숫자로 표현하여 컴퓨터가 의미적 유사성을 계산할 수 있게 해주는 기술
        ○ 문서 백터화 모델
            § RAG기술에 필요 -> 입력값을 벡터로 변환하여 데이터베이스에 저장된 데이터와의 
                            유사도 계산 후 의미적으로 가까운 데이터 검색
        ○ 질의 응답 모델과 다르게 모델 별 큰 성능 차이❌ ➡️ Google Embedding 사용 (무료제공)
        ○ 출력값은 벡터 ➡️ 출력값에 대한 비용 ❌
        ○ MTEB를 참고하여 성능 비교
        
✔️ Token (토큰)
LLM은 사용자로부터 받은 문장을 처리시 token 단위로 분해 처리

✅ 토큰의 계산 방식은 모델과 토크나이저, 언어에 따라 달라질 수 있음

✅ OPEN AI의 경우 tiktoken 라이브러리를 통해 텍스트의 토큰 수를 미리 계산 가능
    1) py py -m pip install tiktoken (패키지 설치)
```
![tiktoken test](<image/tiktoken test.png>)
```

    ✔️ 토큰의 비용 계산
        일반적으로 입력 토큰 수, 출력 토큰 수를 기준으로 계산
        ex) gpt
        입력 토큰 수 X 입력 토큰 단가 + 출력 토큰 수 X 출력 토큰 단가
        
         ✅이미지 인식 기능 or Responses API 관련 기능 사용 시 추가 비용 발생
        
        ✅ Embedding 모델은 텍스트 생성 ❌ / 입력 문장의 고정 길이를 벡터로 변환 역할만 수행
            ➡️ 출력 토큰 개념 ❌ / 입력 텍스트의 토큰 수 기준으로 요금 청구
            
✔️ 학습 데이터
    각 모델의 knowlege cutoff (지식 단절)을 의미 
    ex) 특정 모델이 몇년도 몇월까지의 데이터를 학습 했는가 -> 그 이후의 지식은 가지고 있지 않음
    
     
✔️ Chatbot Arena Score
    Chatbot Arena라는 벤치마크 사이트의 점수
    성능의 기준으로 사용 가능 (영어 기반 평가 플랫폼 -> 참고용으로 사용 할 것)
    
⚠️
비용: 각 기업의 플래그십 모델은 많은 비용이 청구될 가능성이 존재
정보의 최신성: 최신 모델, 요금 등의 정보는 공식 사이트 참고 및 항시 확인 할 것

✔️ Streamlit
    python기반 OSS 프레임워크
    - 대부분의 라이브러리 호환 (pandas, matplotlib, seaborn, plotly, Keras, PyTorch 등)
    
    - Streamlit Cloud 서비스 지원


    - 설치
    1) python -m pip install streamlit
```
![streamlit test](<image/streamlit test.png>)
```
    3) python -m streamlit run ".\AI Agent Leaning\Streamlit_test.py"      
```
![result](<image/streamlit test result.png>)
```
✔️ LangChain
LLM 기반 애플리케이션 개발을 지원하는 라이브러리
다양한 소스에서 데이터 수집, 여러 데이터베이스 연동 기능 제공

    1) 여러 LLM를 간단히 호출
    2) YouTuve, 웹사이트, PDF 등에서 자료 수집
    3) 수집된 데이터를 벡터 DB에 저장
    4) 자율적으로 과제 해결 에이전트 구현

⚠️ 의도치 않은 호환성 문제 방지를 위해 각 라이브러리 버전 고정 권장

    - LangChain 설치
    - python -m pip install langchain
    - python -m pip install langchain-community
    - python -m pip install langchain-core

    -  python -m pip install langchain-openai (gpt)
    -  python -m pip install langchain-anthropic (claude)
    -  python -m pip install langchain-google-genai (gemini)
```