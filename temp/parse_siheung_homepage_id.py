"""
시흥시 main.js 내 HOME_PAGE_ID 상수 값 추출
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

matches = list(re.finditer("HOME_PAGE_ID", txt))
print(f"HOME_PAGE_ID matches: {len(matches)}")

for m in matches[:10]:
    pos = m.start()
    print(f"\n--- Match at pos {pos} ---")
    print(txt[max(0, pos-120):pos+120].strip().replace("\n", " "))
