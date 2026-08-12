"""
광진구립도서관 intro.do Forms 및 JS 파싱
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.gwangjinlib.seoul.kr/intro.do"
r = session.get(url, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("=== Forms ===")
for i, form in enumerate(soup.select("form")):
    print(f"Form[{i}] action='{form.get('action')}' method='{form.get('method')}'")
    for inp in form.select("input, select"):
        print(f"  name='{inp.get('name')}' value='{inp.get('value')}'")

print("\n=== Search Links (all) ===")
for a in soup.select("a"):
    href = a.get("href", "")
    txt = a.text.strip()
    if href and href != "#":
        print(f"  '{txt[:20]}' -> {href}")
