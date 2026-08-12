"""
파주시도서관 topSearchForm 인근 HTML 및 스크립트 분석
"""
from bs4 import BeautifulSoup

with open("paju_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
form = soup.select_one("form#topSearchForm")

if form:
    print("=== topSearchForm prettify ===")
    print(form.prettify()[:1000])
else:
    print("No topSearchForm found")
    
# 스크립트 내 검색 관련 함수 탐색
for idx, sc in enumerate(soup.select("script")):
    txt = sc.text
    if any(w in txt for w in ["search", "topSearch", "submit", "action"]):
        print(f"\n=== Script[{idx}] ===")
        for line in txt.split("\n"):
            if any(w in line for w in ["action", "topSearchForm", "submit", "search", "location"]):
                print("  ", line.strip()[:150])
