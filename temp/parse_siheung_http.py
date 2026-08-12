"""
시흥시 main.js 내 도서 검색 호출 함수 정밀 분석
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# search 단어와 함께 ajax, axios, http, get, post가 함께 쓰이는 구간들 탐색
print("=== axios/http 호출 함수 검색 ===")
# axios.get 또는 axios.post 패턴이나 $http.get 등의 패턴이 있는지 체크
matches_http = re.findall(r"(\.[a-zA-Z0-9_$]+\(['\"]/[a-zA-Z0-9_\-/]+['\"][\s\S]{0,100}\))", txt)
print(f"HTTP calls found: {len(matches_http)}")
for m in sorted(list(set(matches_http)))[:50]:
    if "api" in m or "search" in m or "biblio" in m:
        print("  ", m.strip().replace("\n", " "))
