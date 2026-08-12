"""
안성시도서관 goView 함수 정의부 덤프
"""
from bs4 import BeautifulSoup
import re

with open("anseong_real_result.html", "r", encoding="utf-8") as f:
    html = f.read()

# goView 단어 인근 분석
matches = list(re.finditer(r"function goView", html))
print(f"Matches found: {len(matches)}")

for idx, m in enumerate(matches):
    pos = m.start()
    print(f"\n=== Match {idx} ===")
    print(html[pos:pos+700].replace("\n", " ").strip())
