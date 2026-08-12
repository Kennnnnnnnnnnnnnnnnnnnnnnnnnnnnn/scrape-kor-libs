"""
수원시 모바일 HTML 내부 스크립트 중 AJAX 호출 주소 분석
"""
from bs4 import BeautifulSoup
import re

with open("suwon_mobile.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. Script files linked ===")
for s in soup.select("script[src]"):
    print("Link:", s.get("src"))

print("\n=== 2. Inline scripts parsing ===")
for i, s in enumerate(soup.select("script:not([src])")):
    txt = s.text
    if any(w in txt for w in ["ajax", "url", "post", "get", "search"]):
        print(f"Script[{i}] matches keywords:")
        for line in txt.split("\n"):
            line_s = line.strip()
            if any(w in line_s for w in ["url", "ajax", "type", "action", "data", "Location"]):
                print(f"  {line_s[:120]}")
