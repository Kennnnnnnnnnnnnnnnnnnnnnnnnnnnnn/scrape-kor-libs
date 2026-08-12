"""
하남시 통합검색 영어 단어(python) 기반 POST 실시간 검증
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
    'Referer': 'https://www.hanamlib.go.kr/nalib/index.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

url = "https://www.hanamlib.go.kr/nalib/searchSimple.do"
payload = {
    "searchType": "SIMPLE",
    "searchKey": "ALL",
    "searchCategory": "ALL",
    "key": "64",
    "searchKeyword": "python"
}

try:
    r = session.post(url, data=payload, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("hanam_result_python.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved hanam_result_python.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    titles = soup.select(".title a, a[href*='Detail'], .book_list a, a.book_name, dt.tit a")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:10]):
        print(f"  [{i}] Title: {t.text.strip()} | Href: {t.get('href')}")
        
    print("Keyword count:", r.text.count("python"))
except Exception as e:
    print("Error:", e)
