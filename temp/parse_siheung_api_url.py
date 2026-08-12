"""
시흥시 main.js 내 API_URL 파라미터 검색
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

import re
matches = re.finditer("API_URL", txt)
print("=== API_URL Matches ===")
for m in list(matches)[:30]:
    pos = m.start()
    print(txt[max(0,pos-120):pos+120].strip().replace("\n", " "))
