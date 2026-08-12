"""
광명시도서관 DLS HTML 내 비동기 데이터 바인딩 JS 소스 탐색
"""
from bs4 import BeautifulSoup

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
print(f"Inline script tags: {len(scripts)}")

for i, sc in enumerate(scripts):
    txt = sc.text
    if any(w in txt for w in ["ajax", "load", "$.post", "$.get", "aCallNo"]):
        print(f"\n=== Script[{i}] ===")
        # ajax 호출부 인근 덤프
        for line in txt.split("\n"):
            if any(w in line for w in ["url", "ajax", "post", "get", "aCallNo", "aTitle", "load"]):
                print("  ", line.strip()[:150])
