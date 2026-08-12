"""
순천시립도서관 searchIndex.do 폼 태그 파싱기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://library.suncheon.go.kr/lib/book/search/searchIndex.do?menuCd=L001001001"
r = session.get(url, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("=== Forms ===")
for i, form in enumerate(soup.select("form")):
    print(f"Form[{i}] action='{form.get('action')}' method='{form.get('method')}'")
    for inp in form.select("input, select"):
        print(f"  name='{inp.get('name')}' value='{inp.get('value')}' type='{inp.get('type')}'")
