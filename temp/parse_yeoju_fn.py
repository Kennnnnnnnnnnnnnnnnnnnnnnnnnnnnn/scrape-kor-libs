"""
여주시도서관 fnSearchResultDetail 함수 정의부 덤프
"""
import re

with open("yeoju_result.html", "r", encoding="utf-8") as f:
    html = f.read()

# fnSearchResultDetail 단어 인근 분석
matches = list(re.finditer(r"function fnSearchResultDetail", html))
print(f"Matches found: {len(matches)}")

for idx, m in enumerate(matches):
    pos = m.start()
    print(f"\n=== Match {idx} ===")
    print(html[pos:pos+800].replace("\n", " ").strip())
