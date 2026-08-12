"""
시흥시 main.js 내 인라인 번들된 CONFIG JSON 텍스트 강제 추출
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# "HOME_PAGE_ID" 와 "API_URL" 이 둘 다 인근에 명시된 JSON 패턴 수집
matches = list(re.finditer(r'["\']HOME_PAGE_ID["\']', txt))
print(f"References count: {len(matches)}")

for i, m in enumerate(matches):
    pos = m.start()
    snippet = txt[max(0, pos-250):pos+350]
    # 실제 할당 구조(예: {"HOME_PAGE_ID":"...", "API_URL":"..."} 또는 콜론 할당)인지 판정
    if "API_URL" in snippet and ("{" in snippet or "}" in snippet or ":" in snippet):
        print(f"\n--- Match {i} at pos {pos} ---")
        print(snippet.strip().replace("\n", " "))
