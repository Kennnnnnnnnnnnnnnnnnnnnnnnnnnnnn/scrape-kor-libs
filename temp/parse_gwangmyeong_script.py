"""
광명시도서관 서브밋 함수 스크립트 덤프
"""
from bs4 import BeautifulSoup

with open("gwangmyeong_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
for i, sc in enumerate(scripts):
    txt = sc.text
    if "searchWord" in txt and "alert" in txt:
        print(f"=== Script[{i}] ===")
        print(txt)
