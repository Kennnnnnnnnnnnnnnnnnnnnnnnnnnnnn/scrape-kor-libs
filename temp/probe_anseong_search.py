"""
안성시도서관 검색 URL 엔드포인트 테스트
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
    'Referer': 'https://www.anseong.go.kr/library/main.do'
}

session.get("https://www.anseong.go.kr/library/main.do", headers=HEADERS, timeout=8, verify=False)

candidates = [
    ("https://www.anseong.go.kr/library/search/searchList.do", {"searchTxt": "파이썬", "searchKeyType": "K"}),
    ("https://www.anseong.go.kr/library/search/searchResult.do", {"searchTxt": "파이썬", "searchKeyType": "K"}),
    ("https://www.anseong.go.kr/library/search/searchView.do", {"searchTxt": "파이썬", "searchKeyType": "K"}),
    ("https://www.anseong.go.kr/library/search/bookSearch.do", {"searchTxt": "파이썬"}),
]

for url, params in candidates:
    print(f"\n=== GET {url} ===")
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  Status: {r.status_code}, Length: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")
        if r.status_code == 200 and r.text.count('파이썬') > 0:
            print("  FOUND MATCH!")
            with open("anseong_found.html", "w", encoding="utf-8") as f:
                f.write(r.text)
    except Exception as e:
        print(f"  Error: {e}")

    print(f"=== POST {url} ===")
    try:
        r = session.post(url, data=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  Status: {r.status_code}, Length: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")
        if r.status_code == 200 and r.text.count('파이썬') > 0:
            print("  FOUND MATCH!")
            with open("anseong_found_post.html", "w", encoding="utf-8") as f:
                f.write(r.text)
    except Exception as e:
        print(f"  Error: {e}")
