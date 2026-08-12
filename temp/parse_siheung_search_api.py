"""
시흥시 main.js 내 책 검색 관련 REST API 추출
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# 'api' 단어가 포함된 경로 중 search, book, biblio, item 등의 단어를 포함하는 것들을 필터링
import re
apis = re.findall(r"['\"](/api/[a-zA-Z0-9_\-/]+)['\"]", txt)
unique_apis = sorted(list(set(apis)))

print("=== 책 검색 관련 API 후보 ===")
for api in unique_apis:
    if any(w in api.lower() for w in ["search", "book", "biblio", "item"]):
        print("  ", api)
