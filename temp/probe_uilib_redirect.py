"""
의정부시 도서관(uilib.go.kr) 진짜 리다이렉션 흐름 정밀 분석 (allow_redirects=False)
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

url = "https://www.uilib.go.kr/intro/menu/10008/program/30001/plusSearchResultList.do"

try:
    print("=== 1. Redirect False GET ===")
    r = session.get(url, headers=HEADERS, timeout=8, verify=False, allow_redirects=False)
    print("Status:", r.status_code)
    print("Location Header:", r.headers.get("Location"))
    print("Cookies:", session.cookies.get_dict())
    
    # 만약 Location 이 있다면 거기로 2차 요청
    loc = r.headers.get("Location")
    if loc:
        if loc.startswith("/"):
            loc = "https://www.uilib.go.kr" + loc
        print("\n=== 2. Follow Redirect GET ===")
        r2 = session.get(loc, headers=HEADERS, timeout=8, verify=False, allow_redirects=False)
        print("Status 2:", r2.status_code)
        print("Location Header 2:", r2.headers.get("Location"))
        print("Cookies 2:", session.cookies.get_dict())
        
except Exception as e:
    print("Error:", e)
