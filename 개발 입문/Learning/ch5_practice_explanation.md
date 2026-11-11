# Chapter 5 Practice
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