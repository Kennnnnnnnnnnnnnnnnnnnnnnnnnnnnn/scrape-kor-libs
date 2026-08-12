"""
의정부시 도서관(uilib.go.kr) 프록시 헤더 우회 기반 무한 리다이렉트 탈출 검증
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

# 중요 프록시 우회 헤더 설정!
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'X-Forwarded-Proto': 'https',
    'X-Forwarded-Port': '443',
    'X-Forwarded-Ssl': 'on'
}

url = "https://www.uilib.go.kr/intro/menu/10008/program/30001/plusSearchResultList.do"
params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
    print("Final URL:", r.url)
    print("Status:", r.status_code)
    print("HTML Length:", len(r.text))
    
    if r.status_code == 200 and len(r.text) > 4000:
        print("  [SUCCESS!!!] 200 OK")
        with open("uilib_uijeongbu_search.html", "w", encoding="utf-8") as f:
            f.write(r.text)
except Exception as e:
    print("Error:", e)
