from langchain_text_splitters import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="\n\n", chunk_size=10, chunk_overlap=0  # 분할에 사용하는 구분자
)

print(text_splitter.split_text("안녕하세요\n\n반갑습니다 안녕히가세요"))
