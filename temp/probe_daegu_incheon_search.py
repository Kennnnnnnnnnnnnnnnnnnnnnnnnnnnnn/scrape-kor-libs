"""
인천도서관 및 대구도서관 통합 검색 엔드포인트 세밀 조사
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3

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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

TEST_URLS = [
    # 인천
    "https://www.michuhollib.go.kr/search/searchDetail.do",
    "https://www.michuhollib.go.kr/search/tot/result.do",
    "https://www.michuhollib.go.kr/main/searchBrief",
    "https://www.michuhollib.go.kr/intro/menu/10003/program/30001/searchResultList.do",
    # 대구
    "https://library.daegu.go.kr/search/searchDetail.do",
    "https://library.daegu.go.kr/search/tot/result.do",
    "https://library.daegu.go.kr/main/searchBrief",
    "https://library.daegu.go.kr/intro/menu/10003/program/30001/searchResultList.do"
]

for url in TEST_URLS:
    try:
        r = session.get(url, params={"searchKeyword": "파이썬", "q": "파이썬", "vSrchText": "파이썬"}, headers=HEADERS, timeout=6, verify=False)
        print(f"URL: {url} -> Status: {r.status_code}, Length: {len(r.text)}, error={'요청하신' in r.text or '찾을 수' in r.text or '오류' in r.text}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
