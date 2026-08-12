"""
안양시립도서관 도서 요약 항목 전체 HTML 구조 분석
"""
from bs4 import BeautifulSoup

with open("anyang_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

items = soup.select("#bookList li")
if items:
    print("=== FIRST ITEM HTML ===")
    print(items[0].prettify()[:2500])
