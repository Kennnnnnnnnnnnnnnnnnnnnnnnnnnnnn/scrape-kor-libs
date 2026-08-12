"""
성북구립도서관 library 필드 정제 로직 개선 및
수원시 도서관 SSL 우회 테스트
"""
import re
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# 수원시 도서관 SSL 우회 테스트
print("=== 수원시 도서관 SSL 우회 테스트 ===")
session = requests.Session()
session.mount('https://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    "https://www.suwonlib.go.kr/search/searchDetail.do",
    "https://www.suwonlib.go.kr/search/tot/result.do",
    "https://www.suwonlib.go.kr/intro/menu/10003/program/30001/searchResultList.do",
    "https://www.suwonlib.go.kr/main/searchBrief"
]

for url in urls:
    try:
        r = session.get(url, params={"searchKeyword": "파이썬", "q": "파이썬"}, headers=HEADERS, timeout=8, verify=False)
        print(f"URL: {url} -> Status: {r.status_code}, Length: {len(r.text)}, error_page={'요청하신' in r.text or '찾을 수' in r.text}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
