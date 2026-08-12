"""
울산도서관 도서 리스트 구조 상세 분석
"""
from bs4 import BeautifulSoup

with open("ulsan_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# book_data 후보군 탐색
items = soup.select(".book_data")
print(f"Book items count (by .book_data): {len(items)}")

if not items:
    items = soup.select("ul > li")
    items = [it for it in items if it.select(".book_title")]
    print(f"Book items count (by .book_title parent): {len(items)}")

if items:
    print("\n=== FIRST ITEM HTML ===")
    print(items[0].prettify()[:2500])
else:
    print("No items match classes.")
