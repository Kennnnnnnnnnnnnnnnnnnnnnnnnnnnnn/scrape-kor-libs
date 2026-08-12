"""
의정부시 도서관(uilib.go.kr) 메인 HTML onclick 및 스크립트 분석
"""
from bs4 import BeautifulSoup

with open("uilib_real_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. onclick 속성이 있는 a 태그 상위 30개 ===")
a_clicks = [a for a in soup.select("a") if a.get("onclick")]
for idx, a in enumerate(a_clicks[:30]):
    print(f"  [{idx}] txt='{a.text.strip()}' -> onclick='{a.get('onclick')}' href='{a.get('href')}'")

print("\n=== 2. script 태그 내 function 탐색 ===")
for j, sc in enumerate(soup.select("script")):
    txt = sc.text
    if any(w in txt for w in ["fn_", "link", "move", "menu", "search"]):
        print(f"  Script[{j}] has functions:")
        for line in txt.split("\n"):
            if "function" in line or "location" in line or "href" in line:
                print("    ", line.strip()[:100])
