"""
성북구립도서관 결과 본문 구조 정밀 분석
"""
from bs4 import BeautifulSoup
import re

with open("seongbuk_brief_2.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 총 건수
total_tag = soup.select_one("#totalCnt")
if total_tag:
    print(f"Total count text: {total_tag.text.strip()}")
else:
    print("totalCnt tag not found")

# 도서 목록
items = soup.select("#bookList > div > ul > li")
if not items:
    items = soup.select("#bookList li")
print(f"Book items found: {len(items)}")

if items:
    print("\n=== FIRST ITEM HTML ===")
    print(items[0].prettify()[:1500])
