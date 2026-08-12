"""
SSL 우회 강화 서울 지자체 도서관 검색 진단
"""
import requests
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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive'
}

TARGETS = {
    "강동구립": "https://www.gdlibrary.or.kr",
    "마포구립": "https://www.mplib.mapo.go.kr",
    "동작구립": "https://lib.dongjak.go.kr"
}

# 공통 검색 경로 후보군
PATHS = [
    "/intro/menu/10003/program/30001/searchResultList.do",
    "/intro/menu/10181/program/30012/plusSearchResultList.do",
    "/search/searchDetail.do",
    "/search/tot/result.do"
]

for name, base_url in TARGETS.items():
    print(f"\n--- {name} ({base_url}) ---")
    for path in PATHS:
        url = base_url + path
        try:
            r = session.get(url, params={"searchKeyword": "파이썬", "q": "파이썬"}, headers=HEADERS, timeout=8, verify=False)
            print(f"  Path: {path} -> Status: {r.status_code}, Length: {len(r.text)}")
            if r.status_code == 200 and len(r.text) > 4000:
                print(f"    [SUCCESS] {name} -> {path} (Length: {len(r.text)})")
        except Exception as e:
            print(f"  Path: {path} -> Error: {e}")
