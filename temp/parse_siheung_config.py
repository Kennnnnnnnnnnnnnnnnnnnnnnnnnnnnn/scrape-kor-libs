"""
시흥시 main.js 내 CONFIG 객체 내용 추출
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

import re
matches = list(re.finditer("CONFIG", txt))
print(f"CONFIG matches: {len(matches)}")

# CONFIG = { ... } 또는 CONFIG: { ... } 형태 검색
for m in matches[:15]:
    pos = m.start()
    chunk = txt[max(0, pos-20):pos+600]
    if "API_URL" in chunk or "HOME_PAGE_ID" in chunk:
        print(f"\n--- Match at pos {pos} ---")
        print(chunk.strip().replace("\n", " "))
