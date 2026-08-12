"""
시흥시 main.js 내 searchType 및 params 조립 필드 역추적
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# 'searchType' 이 사용되는 문맥들 탐색
matches = list(re.finditer("searchType", txt))
print(f"searchType matches: {len(matches)}")

for m in matches[:10]:
    pos = m.start()
    print(f"  context:", txt[max(0, pos-100):pos+150].strip().replace("\n", " "))
