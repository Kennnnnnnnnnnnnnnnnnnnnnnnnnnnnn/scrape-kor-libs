"""
군포시 main.js 내 SEARCH_COLLECTION 상수의 실제 값 탐색
"""
import re

with open("gunpo_main.js", "r", encoding="utf-8") as f:
    js = f.read()

# SEARCH_COLLECTION_ 단어들의 오프셋 탐색
matches = [m.start() for m in re.finditer(r"SEARCH_COLLECTION_", js)]
print(f"SEARCH_COLLECTION_ matches: {len(matches)}")

for idx, pos in enumerate(matches[:20]):
    print(f"\n=== Match {idx} (Pos {pos}) ===")
    snippet = js[max(0, pos-150):pos+350]
    print(snippet.strip().replace("\n", " "))
