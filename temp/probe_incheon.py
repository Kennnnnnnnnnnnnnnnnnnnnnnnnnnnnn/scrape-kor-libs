"""
인천광역시교육청도서관(lib.ice.go.kr/ice/index.do) 도서 검색 파싱기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.ice.go.kr/ice/index.do"
r = session.get(url, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("Status:", r.status_code, "Len:", len(r.text))

print("\n=== Forms ===")
for i, form in enumerate(soup.select("form")):
    print(f"Form[{i}] action='{form.get('action')}' method='{form.get('method')}'")
    for inp in form.select("input, select"):
        print(f"  name='{inp.get('name')}' value='{inp.get('value')}' type='{inp.get('type')}'")

print("\n=== Search Links ===")
for a in soup.select("a"):
    href = a.get("href", "")
    txt = a.text.strip()
    if any(k in href.lower() or k in txt for k in ["search", "program", "menu", "검색", "자료"]):
        if 0 < len(txt) < 30:
            print(f"  '{txt}' -> {href}")
