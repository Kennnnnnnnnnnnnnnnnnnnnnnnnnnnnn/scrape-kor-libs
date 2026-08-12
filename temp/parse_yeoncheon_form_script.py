"""
연천군도서관 searchForm 서브밋 자바스크립트 함수 분석
"""
from bs4 import BeautifulSoup

with open("yeoncheon_simple_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 스크립트 중 searchForm 이나 action, submit, search가 들어간 구문 분석
for idx, sc in enumerate(soup.select("script")):
    txt = sc.text
    if any(w in txt for w in ["searchForm", "action", "submit"]):
        print(f"\n=== Script[{idx}] ===")
        for line in txt.split("\n"):
            if any(w in line for w in ["action", "submit", "location", "search", "Form"]):
                print("  ", line.strip()[:150])
