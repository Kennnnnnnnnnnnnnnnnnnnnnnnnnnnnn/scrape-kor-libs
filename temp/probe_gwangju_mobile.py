"""
광주시도서관 모바일 API 및 대체 엔드포인트 탐색
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

mobile_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
}

urls = [
    "https://lib.gjcity.go.kr/m/search/resultList.do",
    "https://lib.gjcity.go.kr/mobile/search/resultList.do",
    "https://lib.gjcity.go.kr/lay1/program/S1T446C461/m/jnet/resourcessearch/resultList.do",
    "https://lib.gjcity.go.kr/kolaseek/search/searchResultList.do",
    "https://lib.gjcity.go.kr/search/resultList.do"
]

params = {
    "searchKeyword": "파이썬",
    "searchType": "SIMPLE"
}

for url in urls:
    try:
        r = session.get(url, params=params, headers=mobile_headers, timeout=8, verify=False)
        print(f"GET {url} -> Status: {r.status_code}, Len: {len(r.text)}, '파이썬': {r.text.count('파이썬')}")
        if r.status_code == 200 and r.text.count('파이썬') > 0:
            print("  ★ FOUND MOBILE GWANGJU MATCH ★")
    except Exception as e:
        print(f"Error: {e}")
