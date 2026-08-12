"""
은평구 /mainSearch.asp 및 /unified/detail_search.asp 파라미터 분석
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    "https://www.eplib.or.kr/mainSearch.asp",
    "https://www.eplib.or.kr/unified/detail_search.asp"
]

for url in urls:
    r = session.get(url, headers=HEADERS, verify=False)
    print(f"URL: {url} -> Status: {r.status_code}, Len: {len(r.text)}")
    soup = BeautifulSoup(r.text, "html.parser")
    for form in soup.select("form"):
        print(f"  Form action='{form.get('action')}' method='{form.get('method')}'")
        for inp in form.select("input, select"):
            print(f"    name='{inp.get('name')}' value='{inp.get('value')}'")
