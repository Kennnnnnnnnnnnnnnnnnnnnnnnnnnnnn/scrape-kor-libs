"""
안성시 GNB 내 통합도서검색 메뉴(0101010000) 근처 href 및 텍스트 덤프
"""
from bs4 import BeautifulSoup

with open("anseong_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 0101010000 이 들어있는 href 찾기
a_tags = soup.select("a[href*='0101']")
print(f"0101 GNB tags: {len(a_tags)}")
for idx, a in enumerate(a_tags):
    print(f"  [{idx}] txt='{a.text.strip()}' -> href='{a.get('href')}'")
