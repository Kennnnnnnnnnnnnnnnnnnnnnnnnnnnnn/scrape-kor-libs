"""
광명시도서관 dd 태그 내부 상세 구조 분석
"""
from bs4 import BeautifulSoup

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

items = soup.select("div.list")
if items:
    print("=== FIRST ITEM DL/DD HTML ===")
    print(items[0].select_one("dl").prettify()[:2500])
