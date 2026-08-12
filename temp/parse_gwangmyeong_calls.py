"""
광명시도서관 HTML 내 getDataDetail 호출부 전방위 검출
"""
import re

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

matches = list(re.finditer(r"getDataDetail\(", html))
print(f"getDataDetail( matches: {len(matches)}")

for i, m in enumerate(matches):
    pos = m.start()
    print(f"\nMatch {i} context:")
    print(html[max(0, pos-250):pos+400].strip().replace("\n", " "))
