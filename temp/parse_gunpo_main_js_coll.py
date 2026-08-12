"""
군포시 main.js 내 collections 및 searchKeyword 인근 코드 덤프
"""
import re

with open("gunpo_main.js", "r", encoding="utf-8") as f:
    js = f.read()

# '/collections/' 단어 검색
matches = [m.start() for m in re.finditer(r"/collections/", js)]
print(f"/collections/ matches count: {len(matches)}")

for idx, pos in enumerate(matches):
    print(f"\n=== /collections/ Match {idx} (Pos {pos}) ===")
    snippet = js[max(0, pos-250):pos+600]
    with open(f"gunpo_coll_snippet_{idx}.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
    print(snippet[:300].strip().replace("\n", " "))
