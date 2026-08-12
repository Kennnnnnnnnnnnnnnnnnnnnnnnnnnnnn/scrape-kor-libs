"""
군포시 main.js 내 retrieve 및 retrieveSearchIssues 실제 사용처 검색 쿼리 빌드 로직 추출
"""
import re

with open("gunpo_main.js", "r", encoding="utf-8") as f:
    js = f.read()

# 'retrieve' 가 호출되거나 search api를 파라미터와 함께 찌르는 곳 탐색
matches = [m.start() for m in re.finditer(r"retrieve\s*\(|retrieveSearchIssues", js)]
print(f"retrieve matches count: {len(matches)}")

for idx, pos in enumerate(matches):
    print(f"\n=== retrieve Match {idx} (Pos {pos}) ===")
    snippet = js[max(0, pos-300):pos+600]
    with open(f"gunpo_retrieve_{idx}.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
    print(snippet[:300].strip().replace("\n", " "))
