"""
의정부시 도서관(uilib.go.kr) 메인 HTML GNB 도서검색 링크 추출
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

# 메인 페이지는 무한 리다이렉트가 도는지 확인하고 allow_redirects=False 로 로드
url = "https://www.uilib.go.kr/"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False, allow_redirects=False)
    print("Status:", r.status_code)
    print("Location:", r.headers.get("Location"))
    
    # 만약 메인도 302 가 난다면, Location 을 타고 들어가며 HTML 낚아채기
    loc = r.headers.get("Location")
    if loc:
        if loc.startswith("/"):
            loc = "https://www.uilib.go.kr" + loc
        r_main = session.get(loc, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
        print("Final Status:", r_main.status_code)
        html = r_main.text
    else:
        html = r.text
        
    soup = BeautifulSoup(html, "html.parser")
    
    # 모든 a 태그의 href 와 text 출력
    links = []
    for a in soup.select("a"):
        href = a.get("href", "")
        txt = a.text.strip().replace("\n", " ")
        if any(w in txt or w in href for w in ["검색", "자료", "search", "book", "lib"]):
            links.append((txt, href))
            
    print(f"\n=== 검색/자료 관련 링크 수집 ({len(links)}개) ===")
    for idx, (t, h) in enumerate(links[:30]):
        print(f"  [{idx}] '{t}' -> {h}")
except Exception as e:
    print("Error:", e)
