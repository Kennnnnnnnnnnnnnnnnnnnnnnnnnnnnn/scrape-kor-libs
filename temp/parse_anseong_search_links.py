"""
안성시 GNB 내 진짜 검색 관련 링크 경로(search/) 전수 식별
"""
from bs4 import BeautifulSoup

with open("anseong_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

a_links = soup.select("a")
print("=== search/ 가 들어간 GNB 링크 수집 ===")
found = 0
for idx, a in enumerate(a_links):
    href = a.get("href", "")
    txt = a.text.strip().replace("\n", " ")
    if "search" in href.lower() or "search" in txt.lower():
        print(f"  [{idx}] txt='{txt[:50]}' -> href='{href}'")
        found += 1
print("Found count:", found)
