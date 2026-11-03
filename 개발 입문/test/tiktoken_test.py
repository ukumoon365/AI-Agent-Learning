import tiktoken

encoding = tiktoken.encoding_for_model("gpt-5")

text = "hello world"
tokens = encoding.encode(text)
print(len(tokens)) # 분할

print(tokens) # 토큰화되는 단위