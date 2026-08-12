"""
김포시도서관 fn_bookSearch 함수 본문 덤프
"""
from bs4 import BeautifulSoup

with open("gimpo_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
for idx, sc in enumerate(scripts):
    txt = sc.text
    if "fn_bookSearch" in txt:
        print(f"=== Script[{idx}] fn_bookSearch ===")
        idx_fn = txt.find("function fn_bookSearch")
        if idx_fn != -1:
            print(txt[idx_fn:idx_fn+1000])
        else:
            print(txt[:1000])
