"""
송파구립도서관 도서 목록 상세 구조 분석
"""
from bs4 import BeautifulSoup

with open("songpa_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# book_dataOuter 또는 bookList 내부 요소 파싱
items = soup.select(".book_dataOuter")
print(f"Items found by .book_dataOuter: {len(items)}")

if not items:
    items = soup.select(".bookList > li")
    print(f"Items found by .bookList > li: {len(items)}")

if items:
    print("\n=== FIRST ITEM HTML ===")
    print(items[0].prettify()[:2500])
else:
    print("No items found.")
