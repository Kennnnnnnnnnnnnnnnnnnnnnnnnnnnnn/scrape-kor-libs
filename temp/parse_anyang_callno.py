"""
안양시립도서관 HTML 내 청구기호 텍스트 구조 상세 탐색
"""
from bs4 import BeautifulSoup

with open("anyang_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# ul.dot-list 또는 li 목록 덤프
items = soup.select("#bookList li")
if items:
    print("=== FIRST BOOK INFO LIST ===")
    info_items = items[0].select("ul.dot-list > li")
    for info in info_items:
        print(f"  Li Text: '{info.text.strip()}'")
