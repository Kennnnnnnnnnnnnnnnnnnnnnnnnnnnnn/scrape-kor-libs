"""
안산시 app.js 내 /api/search API 호출 및 파라미터 구조 파싱
"""
import re

with open("ansan_app.js", "r", encoding="utf-8") as f:
    txt = f.read()

# '/api/search' 근처 문맥 탐색
matches = list(re.finditer(r"['\"]/api/search['\"]", txt))
print(f"/api/search matches: {len(matches)}")

out_lines = []
for m in matches:
    pos = m.start()
    snippet = txt[max(0, pos-250):pos+650]
    out_lines.append(snippet.strip().replace("\n", " "))

with open("ansan_search_parsed.txt", "w", encoding="utf-8") as out:
    for line in out_lines:
        out.write(line + "\n")

print("Saved to ansan_search_parsed.txt")
