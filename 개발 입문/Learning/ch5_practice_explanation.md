# Chapter 5 Practice
## Webpage Summmarizer 
```text
# 웹페이지 관련 패키지
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

✔️ 웹페이지 불러오기
    - requests.get
        웹페이지의 HTML이나 API 데이터를 get
        지금은 웹페이지의 정보를 가져온다

    -   BeautifulSoup()
        HTML 구조 분석 -> HTML 파싱
        ✅ Parsed object (파싱 객체): 데이터를 분석 -> 태그에 구조에 따라 각 요소 구분 및 분석

    -   if문을 통해서 본문일 가능성이 높은 요소 채택
        mian > article > else
 
def get_content(url):
    try:    # 오류 방지 try
        with st.spinner("웹페이지 읽는 중 ⏳"):
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
        st.write(traceback.format_exc())

# URL 유효성 검사 함수
    - urlparse
        URL 문자열을 구성 요소별로 분리하여 구조화된 결과 반환 

    - if문을 통해서 url 유효성 검사

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# URL입력 시 요약 수행
def main():
    
    if url := st.text_input("URL:",key="input"):
        if url != st.session_state.get("previous_url"):
            st.session_state.message_history = [] # url 변경 시 대화 내역 초기화
            is_valid_url = validate_url(url)    # url 유효성 검사
            if not is_valid_url:
                st.write("잘못된 입력입니다. 다시 입력해주세요")
            else:
                if content := get_content(url):
                    st.session_state.summary = summarizer_chain.stream({
                        "content": content,
                        "selected_language": selected_language,
                        "selected_text_length": selected_text_length,
                        })

                    st.session_state.previous_url = url
                    st.session_state.content = content
```
## Youtube Summarizer
```text
def get_content(url):
    with st.spinner("Fetching Youtube ..."):
        try: 
            # 자막 언어 선택
            if select_language == "日本語":
                selected_language = "jp"
            elif select_language == "English":
                selected_language = "en"
            else: selected_language = "ko"

✔️ Youtube 영상의 자막 가져오기
    - YoutubeLoader
        # langchain_community.document_loaders에서 YoutubeLoader import
        ✅ YoutubeLoader는 내부적으로 youtube-transcript-api / pytube를 사용 
            -> 별도 설치 필요
            loader = YoutubeLoader.from_youtube_url(
                url, 
                add_video_info = False, # 불필요한 메타데이터 요청 제거
                language = [selected_language, "en"])

            res = loader.load() ✅ Document 객체를 리스트로 반환

✔️ Document Loader란?
    - LangChain에서 Document Loader는 다양한 소스에서 데이터를 읽기 및 
        언어 모델 처리에 쉬운 표준 구조로 변환 (이 표준 구조를 Document라고 칭함)
    
    - 지원하는 데이터 소스
        1) 데이터 형식 
            CSV, HTML, JSON, PDF, Excel, Word, PowerPoint 등
        2) 서비스
            Youtube, Slack, Discord, Notion, Google Drive, Arxiv 등
        3) 클라우드
            S3, GCS, BigQuery 등
        
        ✅ LangChain 공식 연계 서비스 일람 사이트 참고
        https://integrations.langchain.com

    ✔️ Document란?
        다양한 데이터 소스에서 가져온 내용을 LLM이 바로 처리 가능하도록 정리한 데이터 구조
        하나의 데이터 구조는 두개의 필드로 구성
        1) page_content
            -> str 
            문서의 원본 텍스트 테이터
        2) metadata
            -> dict
            덱스트와 관련된 메타데이터를 키/값으로 저장 (소스 URL. 저자 등등)
        ✅ Documment를 그대로 전달할 시 metadata도 문자열로 반환 후 전달됨 

    ✔️ load / load_and_split
        - load: 설정된 소스에서 문서 전체를 하번에 불러온다
        - load_and_split: 소스에서 문서를 불러온 후 적절한 크기로 텍스트를 나눔

    ✔️ Lazy load(지연 로딩)
        - 문서를 처음부터 메모리에 모두 적재 ❌ 
            -> 필요한 시점에서 필요한 부분만 불러오는 방식
        대규모 문서를 다를 때 메모리 사용량 ⬇️ 

    그 외 다양한 파리미터를 통해 환경과 목적에 맞게 조정 가능 
        
            if res:
                return res[0].page_content
            else:
                return None
        except Exception as e:
            st.error(f"Error occurred: {e}")
            st.write(traceback.format_exc())
            return None
```
```text
# 긴 문서, 긴 영상 요약 

⚠️ 긴 문서, 영상을 요약시 허용되는 최대 토큰 수 초과 오류 발생 가능성 존재 / 긴 콘텐츠일 수록 많은 비용 발생

    - 해결
        1) 긴 콘텐츠를 처리하지 않는다
            - 부분적으로 선택하여 요약한다 
            ex) 앞부분 x개의 토큰만 처리 / 앞과 끝 x개의 토큰을 결합 등
        2) 긴 컨텍스트를 처리 가능한 모델 사용
            - 한번에 요약, 분석 가능 
            - 단가 계산 주의
        3) 긴 텍스트를 분할 후 요약 (MAP REDUCE)
            - 여러 조각으로 분할 뒤 요약 -> 요약본을 통합하는 방식 사용
                1) 긴 문서를 여러 개의 작은 부분으로 분할
                2) 각 조각를 비교적 저렴한 모델으로 1차 요약
                3) 개별 요약본을 합침
                4) 더 고성능 모델로 요약통합본의 전체흐름을 정리하는 2차 요약
                    (고성능의 모델을 최소 단계에서 사용하여 비용 절약)

                    
```