"""
의정부시 도서관(uilib.net) TLS 1.2 강제 및 HTTP 우회 진단
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Tls12Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        # TLS 1.2 강제 및 구버전 cipher 허용
        ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
        ctx.set_ciphers('DEFAULT@SECLEVEL=0')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', Tls12Adapter())
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}

# HTTP 및 HTTPS 둘 다 확인
urls = [
    "http://www.uilib.net/intro/menu/10008/program/30001/plusSearchResultList.do",
    "https://www.uilib.net/intro/menu/10008/program/30001/plusSearchResultList.do"
]

params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

for url in urls:
    print(f"\nURL: {url}")
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
        print(f"  Final URL: {r.url}")
        print(f"  Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 4000:
            print("  [SUCCESS!!!]")
    except Exception as e:
        print(f"  Error: {e}")
