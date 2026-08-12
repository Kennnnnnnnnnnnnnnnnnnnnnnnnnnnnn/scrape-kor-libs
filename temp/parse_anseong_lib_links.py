"""
안성시도서관 GNB 내 모든 /library/ 링크 전수 식별
"""
from bs4 import BeautifulSoup

with open("anseong_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
a_links = soup.select("a")

print("=== /library/ GNB 링크 ===")
found = 0
for idx, a in enumerate(a_links):
    href = a.get("href", "")
    txt = a.text.strip().replace("\n", " ")
    if "/library/" in href:
        print(f"  [{idx}] txt='{txt[:50]}' -> href='{href}'")
        found += 1
print("Total found:", found)
