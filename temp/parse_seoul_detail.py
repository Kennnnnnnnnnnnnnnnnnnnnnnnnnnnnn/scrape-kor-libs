"""
서울도서관 도서 리스트 상세 구조 파싱 테스트
"""
from bs4 import BeautifulSoup

with open("seoul_brief.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

book_list = soup.select_one("ul.list.book-list")
if book_list:
    items = book_list.select("li")
    print(f"Total book items found: {len(items)}")
    if items:
        # 첫 번째 도서의 원본 HTML을 출력
        first_item = items[0]
        print("\n=== FIRST ITEM HTML ===")
        print(first_item.prettify()[:3000])
else:
    print("book-list not found!")
