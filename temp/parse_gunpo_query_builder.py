"""
군포시 main.js 내 Pyxis API 검색 쿼리(params) 빌더 로직 정밀 분석
"""
import re

with open("gunpo_main.js", "r", encoding="utf-8") as f:
    js = f.read()

# 'advanced-search-form' 혹은 'search?' 가 들어가는 컨트롤러/서비스 영역 탐색
matches = [m.start() for m in re.finditer(r"advanced-search-form|/search\?", js)]
print(f"Matches count: {len(matches)}")

for idx, pos in enumerate(matches):
    print(f"\n=== Match {idx} (Pos {pos}) ===")
    snippet = js[max(0, pos-400):pos+800]
    with open(f"gunpo_search_builder_{idx}.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
    print(snippet[:350].strip().replace("\n", " "))
