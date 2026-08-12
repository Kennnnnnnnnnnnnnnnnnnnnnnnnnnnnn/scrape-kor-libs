"""
연천군도서관 /searchResultList.do 실시간 검증
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
    'Referer': 'https://library.yeoncheon.go.kr/index.do'
}

session.get("https://library.yeoncheon.go.kr/index.do", headers=HEADERS, timeout=8, verify=False)

url = "https://library.yeoncheon.go.kr/searchResultList.do"

payload = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

print("=== POST /searchResultList.do ===")
r_post = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
print("POST Status:", r_post.status_code, "Length:", len(r_post.text))
print("POST '파이썬' count:", r_post.text.count("파이썬"))

print("\n=== GET /searchResultList.do ===")
r_get = session.get(url, params=payload, headers=HEADERS, timeout=12, verify=False)
print("GET Status:", r_get.status_code, "Length:", len(r_get.text))
print("GET '파이썬' count:", r_get.text.count("파이썬"))

if r_post.status_code == 200:
    with open("yeoncheon_result.html", "w", encoding="utf-8") as f:
        f.write(r_post.text)
    print("Saved yeoncheon_result.html")

    soup = BeautifulSoup(r_post.text, "html.parser")
    print("items (dl/li/tr):", len(soup.select("dl, li, tr")))
