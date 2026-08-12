"""
시흥시 main.js 내 HOME_PAGE_ID 상수 정의 위치 탐색 2
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# HOME_PAGE_ID : '...' 또는 "..." 또는 = '...' 형태 탐색
matches = list(re.finditer("HOME_PAGE_ID", txt))
print(f"Total HOME_PAGE_ID matches: {len(matches)}")

out_lines = []
for m in matches[10:50]:  # 다른 영역의 인근 코드 확인
    pos = m.start()
    snippet = txt[max(0, pos-120):pos+120]
    out_lines.append(snippet.strip().replace("\n", " "))

with open("siheung_hpid_parsed.txt", "w", encoding="utf-8") as out:
    for line in out_lines:
        out.write(line + "\n")

print("Saved to siheung_hpid_parsed.txt")
