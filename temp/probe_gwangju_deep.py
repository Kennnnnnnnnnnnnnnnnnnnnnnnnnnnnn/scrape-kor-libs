"""
경기도 광주시도서관 검색 결과 파싱 시도 (테이블/리스트 등 다양한 구조)
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SslAdapter())
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.gjcity.go.kr/'
}

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
params = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
print("Status:", r.status_code)
print("Length:", len(r.text))

with open("gwangju_real_result2.html", "w", encoding="utf-8") as f:
    f.write(r.text)

soup = BeautifulSoup(r.text, "html.parser")

# 모든 결과 구조 후보 검색
for sel in ["div.resultListItem", "table tr", "ul li", "div.book_list", 
            "div.search_result", "div.searchList", "a[href*='Detail']",
            "a[onclick*='Detail']", "a[onclick*='detail']", "a[href*='detail']"]:
    items = soup.select(sel)
    if items:
        print(f"  '{sel}': {len(items)} items")

print(f"\n'파이썬' in text: {r.text.count('파이썬')}")
print(f"'청구기호' in text: {r.text.count('청구기호')}")

# 첫 번째 form 의 하위 input 출력
forms = soup.select("form")
for i, form in enumerate(forms[:3]):
    print(f"\nForm[{i}] action='{form.get('action')}' id='{form.get('id')}'")
    for inp in form.select("input")[:15]:
        print(f"  name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
