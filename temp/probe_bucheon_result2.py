"""
부천시도서관 이중 인코딩 우회 최종 검색 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import urllib.parse

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
    'Referer': 'https://alpasq.bcl.go.kr/alpasq-kolas-daemon/sso/bcl/sso.jsp'
}

proc_url = "https://alpasq.bcl.go.kr/alpasq-kolas-daemon/sso/bcl/ssoProc.jsp"

# requests가 form-urlencoded 인코딩을 알아서 처리하도록 "파이썬" 한글 문자열 그대로 대입!
payload = {
    "pni_client_ip": "127.0.0.1",
    "route": "SEARCH",
    "keyword": "파이썬",
    "param": ""
}

try:
    # 1. SSO Proc 세션 획득
    r_proc = session.post(proc_url, data=payload, headers=HEADERS, timeout=8, verify=False)
    print("Proc Status:", r_proc.status_code)
    
    # 2. 진짜 검색 결과 페이지 로드 (여기서는 URL에 수동 인코딩 필요)
    keyword_enc = urllib.parse.quote("파이썬")
    search_url = f"https://alpasq.bcl.go.kr/search/keyword/{keyword_enc}"
    r = session.get(search_url, headers=HEADERS, timeout=10, verify=False)
    
    print("Search Status:", r.status_code)
    print("Search Length:", len(r.text))
    
    with open("bucheon_result2.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    titles = soup.select("a.book_name, .bookArea a.book_name, .book_name a, .title a, a[href*='Detail']")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()}")
        
    # '파이썬' 단어 카운트
    print("Keyword count:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
