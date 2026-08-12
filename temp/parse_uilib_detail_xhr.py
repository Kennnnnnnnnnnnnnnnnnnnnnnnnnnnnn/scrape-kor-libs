"""
의정부도서관 상세페이지 HTML 내 소장현황 비동기 API(XHR) 주소 분석
"""
from bs4 import BeautifulSoup

with open("uijeongbu_detail.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
print(f"Inline script tags: {len(scripts)}")

for i, sc in enumerate(scripts):
    txt = sc.text
    if any(w in txt for w in ["ajax", "load", "$.post", "$.get", "post", "get", "HTML", "html"]):
        print(f"\n=== Script[{i}] ===")
        for line in txt.split("\n"):
            if any(w in line for w in ["url", "ajax", "post", "get", "Detail", "load", "html", "location"]):
                print("  ", line.strip()[:150])
