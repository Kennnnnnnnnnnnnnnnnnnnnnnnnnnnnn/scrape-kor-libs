"""
군포시 main.js 내 SEARCH_COLLECTION 상수의 실제 값 탐색 (정밀 검색)
"""
import re

with open("gunpo_main.js", "r", encoding="utf-8") as f:
    js = f.read()

# "SEARCH_COLLECTION_COMMON" 단어의 모든 매치 검색
matches = [m.start() for m in re.finditer(r"SEARCH_COLLECTION_COMMON\s*[:=]", js)]
if not matches:
    # 느슨하게 매치 검색
    matches = [m.start() for m in re.finditer(r"SEARCH_COLLECTION_COMMON", js)]

print(f"Matches count: {len(matches)}")
for idx, pos in enumerate(matches):
    print(f"\n=== Match {idx} (Pos {pos}) ===")
    snippet = js[max(0, pos-100):pos+300]
    print(snippet.strip().replace("\n", " "))
