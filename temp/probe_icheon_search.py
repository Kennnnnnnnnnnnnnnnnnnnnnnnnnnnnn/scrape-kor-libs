"""
이천시도서관 통합검색(search/tot/result) GET 실시간 검증 (SyntaxError 수정)
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
    'Referer': 'https://www.icheonlib.go.kr/'
}

url = "https://www.icheonlib.go.kr/search/tot/result"
params = {
    "si": "TOTAL",
    "st": "KWRD",
    "q": "파이썬"
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("icheon_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved icheon_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    titles = soup.select(".title a, a[href*='search/detail'], .book_list a, a.book_name, dt.tit a, div.title, div.tit")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:15]):
        txt = t.text.strip().replace('\n', ' ')
        print(f"  [{i}] Title: {txt}")
        
    print("Keyword count:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
