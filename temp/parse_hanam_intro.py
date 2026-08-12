"""
하남시 인트로 페이지 내 링크 전수 파싱
"""
from bs4 import BeautifulSoup

with open("hanam_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

a_tags = soup.select("a")
print(f"Total a tags: {len(a_tags)}")

for idx, a in enumerate(a_tags):
    href = a.get("href", "")
    txt = a.text.strip().replace("\n", " ")
    print(f"  [{idx}] href='{href}' | txt='{txt[:50]}'")
