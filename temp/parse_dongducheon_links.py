"""
동두천시 GNB 내 통합도서검색 및 자료검색 관련 링크(/ddclib/) 전수 식별
"""
from bs4 import BeautifulSoup

with open("dongducheon_real_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

a_links = soup.select("a")
print("=== /ddclib/ GNB 링크 ===")
found = 0
for idx, a in enumerate(a_links):
    href = a.get("href", "")
    txt = a.text.strip().replace("\n", " ").replace("\t", " ")
    if "/ddclib/" in href and any(w in href.lower() or w in txt.lower() for w in ["book", "search", "자료"]):
        print(f"  [{idx}] txt='{txt[:50]}' -> href='{href}'")
        found += 1
print("Total found:", found)
