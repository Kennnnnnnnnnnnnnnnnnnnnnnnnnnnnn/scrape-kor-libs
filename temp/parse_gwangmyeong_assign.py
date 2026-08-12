"""
광명시도서관 HTML 내 dataDetail 값 할당 위치 탐색
"""
import re

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

matches = list(re.finditer(r"dataDetail\[", html))
print(f"dataDetail[ matches: {len(matches)}")

for i, m in enumerate(matches):
    pos = m.start()
    print(f"\nMatch {i} context:")
    print(html[pos:pos+400].strip().replace("\n", " "))
