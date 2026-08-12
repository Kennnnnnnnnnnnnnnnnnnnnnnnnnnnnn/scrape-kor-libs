"""
시흥시 main.js 내 biblios 목록 검색 파라미터 구조 파싱
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# biblios 가 포함된 ajax/get/post 구문 찾기
matches = list(re.finditer("biblios", txt))
for m in matches:
    pos = m.start()
    snippet = txt[max(0, pos-200):pos+600]
    # url... biblios ... 형태의 API 호출 코드 확인
    if "API_URL" in snippet and ("params" in snippet or "data" in snippet or "get" in snippet):
        print("\n--- Match ---")
        print(snippet.strip().replace("\n", " "))
