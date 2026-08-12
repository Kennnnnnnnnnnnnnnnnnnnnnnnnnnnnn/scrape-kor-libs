"""
동작구립도서관 dj/index.do 진짜 페이지 폼 및 스크립트 파싱
"""
import requests
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.dongjak.go.kr/dj/index.do"
r = session.get(url, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print(f"Status: {r.status_code}, Length: {len(r.text)}")

print("\n=== Forms ===")
for i, form in enumerate(soup.select("form")):
    print(f"Form[{i}] id='{form.get('id')}' action='{form.get('action')}' method='{form.get('method')}'")
    for inp in form.select("input, select"):
        print(f"  name='{inp.get('name')}' value='{inp.get('value')}' type='{inp.get('type')}'")

print("\n=== Script search matches ===")
for sc in soup.select("script"):
    txt = sc.text
    if "search" in txt.lower() or "submit" in txt.lower():
        for line in txt.split("\n"):
            line_s = line.strip()
            if any(k in line_s.lower() for k in ["search", "action", "location", "href", "fn_"]):
                print(" ", line_s[:120])
