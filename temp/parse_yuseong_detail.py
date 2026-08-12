"""
유성구립도서관 결과 페이지 상세 구조 파싱
"""
from bs4 import BeautifulSoup

with open("yuseong_brief_2.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 총 건수
total_tag = soup.select_one("#totalCnt")
if total_tag:
    print(f"Total count tag text: {total_tag.text.strip()}")
else:
    print("totalCnt not found")

# 도서 목록
items = soup.select("#bookList > div > ul > li")
if not items:
    items = soup.select("#bookList li")
print(f"Book items count: {len(items)}")

if items:
    print("\n=== FIRST ITEM HTML ===")
    print(str(items[0])[:2000])
