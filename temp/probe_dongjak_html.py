"""
dongjak_full_ok.html 파일 상세 파싱
"""
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("dongjak_full_ok.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# h1, h2, h3, h4, div, li, td 등 모든 텍스트 단서 추출
print("=== All text snippets in dongjak_full_ok.html ===")
for i, el in enumerate(soup.find_all(["div", "li", "tr", "td", "span", "a", "strong"])):
    txt = el.text.strip().replace("\n", " ")
    if len(txt) > 10 and len(txt) < 150:
        if any(k in txt for k in ["도서", "청구", "저자", "발행", "소장", "대출", "자료"]):
            print(f"[{i}] <{el.name}> class={el.get('class')}: {txt}")
