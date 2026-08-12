"""
시흥시 main.js 내 CONFIG 상수 선언부 추출
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

import re
matches = list(re.finditer(r'constant\s*\(\s*["\']CONFIG["\']', txt))
print(f"constant('CONFIG') matches: {len(matches)}")

for m in matches:
    pos = m.start()
    print(f"\n--- Match at pos {pos} ---")
    print(txt[pos:pos+1500].strip().replace("\n", " "))
