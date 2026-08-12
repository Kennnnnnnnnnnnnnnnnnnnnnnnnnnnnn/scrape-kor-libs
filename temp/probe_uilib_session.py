"""
의정부시 도서관 수동 세션 바인딩을 통한 무한 리다이렉트 우회 검증
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
params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

try:
    print("=== 1. JSESSIONID 쿠키 획득 (allow_redirects=False) ===")
    r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False, allow_redirects=False)
    print("  Status:", r.status_code)
    cookies = session.cookies.get_dict()
    print("  Acquired Cookies:", cookies)
    
    # 획득한 쿠키를 세션에 확실하게 강제 고정!
    # 그리고 allow_redirects=False 로 HTTPS 타깃을 찌름!
    # (세션이 이미 톰캣에 성립되었으므로, 더이상 http 로 302 강제를 타지 않고 200이 뜰 수 있습니다!)
    if 'JSESSIONID' in cookies:
        print("\n=== 2. 세션 고정 후 HTTPS 직접 찌르기 (allow_redirects=False) ===")
        # 톰캣의 세션 무한 루프 차단을 유도하기 위해 리다이렉트 비활성인 채로 한 번 더 요청
        r2 = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False, allow_redirects=False)
        print("  Status 2:", r2.status_code)
        print("  Location Header 2:", r2.headers.get("Location"))
        
        # 만약 Status 2 가 200 이라면 완전 대성공!
        # 혹은 계속 302 가 난다면 Location 을 다르게 뚫어야 함
        
except Exception as e:
    print("Error:", e)
