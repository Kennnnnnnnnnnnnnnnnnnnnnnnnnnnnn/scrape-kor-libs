"""
의왕시도서관 info02 내부 span 태그 상세 분석
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
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
    'Referer': 'https://www.uwlib.or.kr/intro/index.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

session.get("https://www.uwlib.or.kr/intro/index.do", headers=HEADERS, timeout=8, verify=False)

url = "https://www.uwlib.or.kr/jungang/program/searchResultList.do"
payload = {
    "searchType": "SIMPLE", "searchCategory": "ALL", "searchField": "ALL",
    "searchWord": "파이썬", "searchLibrary": "ALL",
    "searchPbLibrary": "ALL", "searchSmLibrary": "ALL"
}

r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

items = soup.select("ul.listWrap > li:not(.noResultNote)")

for i, item in enumerate(items[:3]):
    data_inner = item.select_one("div.book_dataInner")
    if not data_inner:
        continue
    
    info02 = data_inner.select_one("div.info02")
    info03 = data_inner.select_one("div.info03")
    
    if info02:
        inner_div = info02.select_one("div")
        if inner_div:
            spans = inner_div.find_all("span")
            print(f"\n=== Item [{i}] info02 inner div spans: {len(spans)} ===")
            for j, sp in enumerate(spans):
                print(f"  span[{j}]: class={sp.get('class', [])} text='{sp.text.strip()}'")
            # 만약 span이 없으면, 원본 html 확인
            if not spans:
                print(f"  Raw HTML: {str(inner_div)[:300]}")
    
    if info03:
        inner_div = info03.select_one("div")
        if inner_div:
            spans = inner_div.find_all("span")
            print(f"  info03 spans: {len(spans)}")
            for j, sp in enumerate(spans):
                print(f"    span[{j}]: class={sp.get('class', [])} text='{sp.text.strip()}'")
            if not spans:
                print(f"  info03 Raw HTML: {str(inner_div)[:300]}")
