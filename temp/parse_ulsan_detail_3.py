"""
울산도서관 부모 컨테이너 및 전체 아이템 구조 파싱
"""
from bs4 import BeautifulSoup

with open("ulsan_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# book_data 의 부모 태그를 찾아서 출력
bd = soup.select_one(".book_data")
if bd:
    parent = bd.parent
    print(f"Parent tag: <{parent.name}> class={parent.get('class')}")
    print("\n=== Parent HTML ===")
    print(parent.prettify()[:2500])
else:
    print("book_data not found")
