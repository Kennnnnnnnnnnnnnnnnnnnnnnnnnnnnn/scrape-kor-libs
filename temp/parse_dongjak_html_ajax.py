"""
동작구립 검색결과 HTML 내 AJAX 로딩 URL 탐색
"""
from bs4 import BeautifulSoup
import re

with open("dongjak_search_with_libs.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. Script 내 URL/AJAX 분석 ===")
scripts = soup.select("script")
for i, sc in enumerate(scripts):
    txt = sc.text
    if any(w in txt for w in ["ajax", "load", "url", "doAjax"]):
        print(f"Script[{i}]:")
        for line in txt.split("\n"):
            if any(w in line for w in ["load", "ajax", "url", "index.do", "list.do", ".do"]):
                print("  ", line.strip()[:150])
