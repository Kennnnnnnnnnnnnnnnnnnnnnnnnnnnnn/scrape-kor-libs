"""
시흥시 main.js 내 HOME_PAGE_ID 할당문 탐색
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# HOME_PAGE_ID = ... 또는 HOME_PAGE_ID: ... 근처 문맥 출력
matches = list(re.finditer("HOME_PAGE_ID", txt))
for m in matches:
    pos = m.start()
    snippet = txt[max(0, pos-10):pos+60]
    if "=" in snippet or ":" in snippet:
        print("Snippet:", snippet.strip().replace("\n", " "))
