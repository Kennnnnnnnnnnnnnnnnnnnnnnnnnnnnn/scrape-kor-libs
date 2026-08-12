"""
동작구 librarySearch 및 모든 Form input 태그 상세 파싱
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.dongjak.go.kr/dj/intro/search/index.do"
r = session.get(url, params={"menu_idx": "111"}, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("=== All Forms in Search Page ===")
for i, form in enumerate(soup.select("form")):
    print(f"\nForm[{i}] id='{form.get('id')}' action='{form.get('action')}' method='{form.get('method')}'")
    for inp in form.select("input, select, textarea"):
        print(f"  <{inp.name}> name='{inp.get('name')}' value='{inp.get('value')}' type='{inp.get('type')}'")
