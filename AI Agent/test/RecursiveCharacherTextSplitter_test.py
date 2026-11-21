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