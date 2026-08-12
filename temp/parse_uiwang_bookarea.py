"""
의왕시도서관 bookArea 하위 구조 정밀 파싱 테스트
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
print(f"Items: {len(items)}")

for i, item in enumerate(items[:5]):
    book_area = item.select_one("div.bookArea")
    if not book_area:
        continue
    
    # 모든 하위 태그를 상세히 분석
    all_children = book_area.find_all(recursive=False)
    print(f"\n=== Item [{i}] bookArea children: {len(all_children)} ===")
    for j, ch in enumerate(all_children):
        cls = ch.get("class", [])
        tag = ch.name
        # 재귀적으로 하위 태그 확인
        inner = ch.find_all(recursive=False)
        txt = ch.get_text(separator='|', strip=True)[:150]
        print(f"  [{j}] <{tag}> class={cls} children={len(inner)}: '{txt}'")
        for k, inn in enumerate(inner[:10]):
            icls = inn.get("class", [])
            itxt = inn.get_text(strip=True)[:80]
            print(f"    [{k}] <{inn.name}> class={icls}: '{itxt}'")
