"""
송파구립도서관 모든 a 태그 목록 및 href 구조 덤프
"""
from bs4 import BeautifulSoup

with open("songpa_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 클래스명 목록들 덤프
classes = set()
for tag in soup.find_all(True):
    cls = tag.get("class")
    if cls:
        classes.add(" ".join(cls))
print("Found Classes:", list(classes)[:40])

# a 태그 중 글자가 있는 링크 상위 20개 출력
print("\n=== Top 20 links ===")
for a in soup.select("a")[:30]:
    txt = a.text.strip()
    if txt:
        print(f"  a href='{a.get('href')}' text='{txt[:50]}'")
