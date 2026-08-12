"""
시흥시 main.js 내 biblios API 호출 엔드포인트 역추적
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# biblios 단어가 들어간 텍스트 라인 전부 탐색
matches = list(re.finditer("biblios", txt))
print(f"biblios matches: {len(matches)}")

for m in matches[:15]:
    pos = m.start()
    print(f"\n--- Match at pos {pos} ---")
    print(txt[max(0, pos-120):pos+120].strip().replace("\n", " "))
