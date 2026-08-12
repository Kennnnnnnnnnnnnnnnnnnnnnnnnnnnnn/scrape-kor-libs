"""
안성시도서관 search.do?mId=0101010100 검증
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
    'Referer': 'https://www.anseong.go.kr/library/main.do'
}

session.get("https://www.anseong.go.kr/library/main.do", headers=HEADERS, timeout=8, verify=False)

url = "https://www.anseong.go.kr/library/search/search.do?mId=0101010100"
payload = {
    "searchKeyType": "K",
    "searchTxt": "파이썬"
}

print("=== POST 요청 ===")
r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
print("Status:", r.status_code, "Length:", len(r.text))
print("'파이썬' count:", r.text.count("파이썬"))

if r.status_code == 200:
    with open("anseong_search_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved anseong_search_result.html")

    soup = BeautifulSoup(r.text, "html.parser")
    # 파싱 구조 확인
    items = soup.select("ul.resultList li, table tbody tr, div.bookList li, div.searchResult li, div.result_list li, div.book_info")
    print("Items found:", len(items))
