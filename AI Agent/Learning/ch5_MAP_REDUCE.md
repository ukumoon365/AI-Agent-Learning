## MAP_REDUCE
```text
def init_chain(summarize_chain):
    ✔️ Text Splitter  
    긴 텍스트를 청크(작은 덩어리) 단위로 분할하는 도구
    (긴 문서를 분석 / LLM의 토큰 제한을 넘기지 않도록 텍스트를 나눌 때 주로 사용)
    
    Text Splitter에는 여러 종류가 존재 -> 규칙이나 길이를 계산하는 기준에 따라 적합하게 선택 및 사용
    1) CharacterTextSplitter
    문자 단위로 텍스트 분할하는 기본적인 Text Splitter
    \n\n 단위 ( 2개의 줄 바꿈)을 기준으로 나누고 
    청크 크기 = 문자 수
    
    ⭐ chunk_overlap
    인접한 청크 사이로 일부 텍스틀 겹치게 하는 기능을 가진 매개 변수
    청크 간의 흐름을 유지하고 싶을 때 사용
    from langchain_text_splitters import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n\n", chunk_size=10, chunk_overlap=0  # 분할에 사용하는 구분자
    )
    print(text_splitter.split_text("안녕하세요\n\n반갑습니다 안녕히가세요"))
    
    ['안녕하세요',  '반갑습니다 안녕히가세요']
    ⚠️ 구분자 없는 문서는 분할 ❌
    
    ⚠️ character TextSplitter는 분할 규칙이 단순 -> 유연성 부족
    
    2) RecursiveCharacterTextSplitter
    여러 구분자를 사용해 재귀적으로 텍스트를 분할하는 도구
    기분 구분자는 {"\n\n", "\n", " ",""] 순서로 적용
    ✅ separators 파라미터로 구분자 변경 가능
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 60,
        chunk_overlap = 20,
        separators=["\n\n", "\n", " ",""] # 기본 값
    )
    text = "생성형 AI와 AI 에이전트(또는 에이전트 AI)의 가장 큰 차이점은 질문에 답하는 수동적 존재 인지, 목표를 위해 스스로 일하는 능동적 존재 인지에 있습니다. \
    1. 생성형 AI (Generative AI) \
    핵심 역할: 사용자의 프롬프트(명령)에 반응하여 텍스트, 이미지, 코드 등 새로운 콘텐츠를 생성하는 '대답하는 AI'입니다. \
    상호작용: 사용자가 먼저 질문하거나 명령을 내려야만 작동하는 반응형입니다."
    print(text_splitter.split_text(text))
    
    ['생성형 AI와 AI 에이전트(또는 에이전트 AI)의 가장 큰 차이점은 질문에 답하는 수동적 존재 인지,', '질문에 답하는 수동적 존재 인지, 목표를 위해 스스로 일하는 능동적 존재 인지에 있습니다. 1. 생성형', '존재 인지에 있습니다. 1. 생성형 AI (Generative AI) 핵심 역할: 사용자의', 'AI) 핵심 역할: 사용자의 프롬프트(명령)에 반응하여 텍스트, 이미지, 코드 등 새로운 콘텐츠를 생성하는', "코드 등 새로운 콘텐츠를 생성하는 '대답하는 AI'입니다. 상호작용: 사용자가 먼저 질문하거나 명령을", '사용자가 먼저 질문하거나 명령을 내려야만 작동하는 반응형입니다.']
    
    ✔️ tiktoken_encoder 
    토큰 개수 기준으로 텍스트를 분할하는 도구
    ⚠️ 문자 수 기준으로 청크를 계산하면 토큰 제한 초과 문제 발생 가능성 존재 (ex: 한글은 영어의 2배로 계산 되는 경우)
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-5", # 토큰 계산 방식의 기준이 될 모델 지정
        chunk_size = 60,
        chunk_overlap = 0,
    )
    text = "생성형 AI와 AI 에이전트(또는 에이전트 AI)의 가장 큰 차이점은 질문에 답하는 수동적 존재 인지, 목표를 위해 스스로 일하는 능동적 존재 인지에 있습니다. \
    1. 생성형 AI (Generative AI) \
    핵심 역할: 사용자의 프롬프트(명령)에 반응하여 텍스트, 이미지, 코드 등 새로운 콘텐츠를 생성하는 '대답하는 AI'입니다. \
    상호작용: 사용자가 먼저 질문하거나 명령을 내려야만 작동하는 반응형입니다."
    print(text_splitter.split_text(text))
    
    ['생성형 AI와 AI 에이전트(또는 에이전트 AI)의 가장 큰 차이점은 질문에 답하는 수동적 존재 인지, 목표를 위해 스스로 일하는 능동적 존재 인지에 있습니다. 1. 생성형 AI', "(Generative AI) 핵심 역할: 사용자의 프롬프트(명령)에 반응하여 텍스트, 이미지, 코드 등 새로운 콘텐츠를 생성하는 '대답하는 AI'입니다. 상호작용: 사용자가 먼저 질문하거나 명령을 내려야만", '작동하는 반응형입니다.']
    
     ✔️ 그 외 
    1) LatexTextSplitter / MarkdownTextSplitter : 특정 형식에 특화 / 각각의 형식으로 정의된 레이아웃 요소를 바탕으로 텍스트 분할 -> 의미있는 구조 유지 가능
    2) CodeTextsplitter: 여러가지 프로그래밍 언어를 지원하여 적절한 코드 분할 가능
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-5", # tiktoken 토큰 계산에 사용할 모델 지정

        chunk_size=16000, # 하나의 청크에 포함할 최대 토큰 수
        chunk_overlap = 0, # 요약에는 중복 불필요
    )
```
# RunnableLambda
    LangChain에 내장에 정의되지 않은 임의 함수를 chain에서 사용할 수 있도록 하는 기능
ex)
to_upper = RunnableLambda(to_upper): Lambda에 감싸서 사용
to_upper = RunnableLambda(lambda x: {"content": x["content"].upper()}): Lambda식 사용

✔️ .map()
    -   체인 내부에서 리스트의 각 요소를 chain()에 적용하고 결과값을 다시 리스트로 반환
    ✅ .batch(): 체인 외부에서 여러 입력을 한 번에 실행 ex) chain.batch(["input 1", "input 2" ....])
