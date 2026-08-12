"""
의왕시도서관 book_dataInner 내부 span 태그 상세 분석
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
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchField": "ALL",
    "searchWord": "파이썬",
    "searchLibrary": "ALL",
    "searchPbLibrary": "ALL",
    "searchSmLibrary": "ALL"
}

r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

items = soup.select("ul.listWrap > li:not(.noResultNote)")

for i, item in enumerate(items[:3]):
    data_inner = item.select_one("div.book_dataInner")
    if not data_inner:
        continue
    
    print(f"\n=== Item [{i}] book_dataInner ===")
    all_tags = data_inner.find_all(recursive=False)
    for j, tag in enumerate(all_tags):
        cls = tag.get("class", [])
        txt = tag.get_text(strip=True)[:80]
        print(f"  [{j}] <{tag.name}> class={cls}: '{txt}'")
        # 하위 태그
        for k, sub in enumerate(tag.find_all(recursive=False)):
            scls = sub.get("class", [])
            stxt = sub.get_text(strip=True)[:60]
            print(f"    [{k}] <{sub.name}> class={scls}: '{stxt}'")
