"""
연천군도서관 상세검색 파라미터 테스트
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
    'Referer': 'https://library.yeoncheon.go.kr/index.do'
}

session.get("https://library.yeoncheon.go.kr/index.do", headers=HEADERS, timeout=8, verify=False)

url = "https://library.yeoncheon.go.kr/searchResultList.do"

payload_variants = [
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchKeyword": "파이썬", "searchWordTitle": "파이썬"},
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "TITLE", "searchKeyword": "파이썬", "searchWordTitle": "파이썬"},
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchKeyword": "파이썬", "searchWordKeyword": "파이썬"},
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchKeyword": "파이썬", "searchWordTitle": "파이썬", "searchLibrary": "ALL", "searchPbLibrary": "ALL", "searchSmLibrary": "ALL"},
]

for idx, p in enumerate(payload_variants):
    print(f"\n=== Variant [{idx}] ===")
    r = session.post(url, data=p, headers=HEADERS, timeout=12, verify=False)
    print(f"Status: {r.status_code}, Length: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")
    if r.status_code == 200 and len(r.text) > 1000:
        print("  FOUND RESULTS!")
        with open(f"yeoncheon_success_{idx}.html", "w", encoding="utf-8") as f:
            f.write(r.text)
