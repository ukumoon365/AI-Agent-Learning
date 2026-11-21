## Web Summarizer
```text
1. 프로젝트 소개

LangChain과 Streamlit을 활용하여 개발한 웹페이지 요약 및 질의응답 애플리케이션입니다.

사용자가 입력한 URL의 웹페이지 내용을 추출하여 원하는 언어와 분량으로 요약하며, 요약한 내용을 바탕으로 추가 질문과 답변을 주고받을 수 있습니다.

배포 주소

Demo: https://kyeong-web-summarizer.streamlit.app/

GitHub: https://github.com/ukumoon365/AI-Agent-Learning/tree/main/%EA%B0%9C%EB%B0%9C%20%EC%9E%85%EB%AC%B8/web_summarizer

2. 주요 기능

웹페이지 URL 입력 및 유효성 검사

웹페이지 본문 추출 기능

여러 LLM 모델 선택 기능

요약 결과의 언어 선택 기능 (한국어, 일본어, 영어)

요약 분량 조절 기능

웹페이지 핵심 내용 요약 기능

요약한 웹페이지 내용을 바탕으로 한 추가 질의응답 기능

대화 기록 유지 기능

대화 내역 삭제 기능

3. 주의사항

API 사용량 및 비용 문제로 인해 현재 Google Gemini 모델 사용을 권장합니다.

코드에는 Gemini, GPT, Claude 모델 선택 기능이 구현되어 있으며, 각 모델을 사용하려면 해당 제공자의 API 키가 필요합니다.
```