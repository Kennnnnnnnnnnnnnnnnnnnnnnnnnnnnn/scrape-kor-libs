"""
광주시도서관 check 및 check1 함수 본문 정밀 분석
"""
from bs4 import BeautifulSoup

with open("gwangju_real_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

for idx, sc in enumerate(soup.select("script")):
    txt = sc.text
    if "function check" in txt or "check1" in txt:
        print(f"=== Script[{idx}] check ===")
        print(txt)
