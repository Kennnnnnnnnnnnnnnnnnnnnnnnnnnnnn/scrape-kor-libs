"""
시흥시 main.js 내 collections/{id}/search 호출부 쿼리스트링(i) 조립 역추적
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# "/collections/" + ... + "/search" 패턴 탐색
matches = list(re.finditer(r"/collections/[^/]+/search", txt))
print(f"Matches count: {len(matches)}")

out_lines = []
for m in matches:
    pos = m.start()
    # 인근 600바이트를 덤프
    snippet = txt[max(0, pos-400):pos+600]
    out_lines.append(snippet.strip().replace("\n", " "))

with open("siheung_search_query_parsed.txt", "w", encoding="utf-8") as out:
    for line in out_lines:
        out.write(line + "\n\n")

print("Saved to siheung_search_query_parsed.txt")
