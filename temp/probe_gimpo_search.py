"""
김포시도서관 통합검색(bookSearchList.do) POST 실시간 검증
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
    'Referer': 'https://www.gimpo.go.kr/lib/index.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

url = "https://www.gimpo.go.kr/lib/bookSearchList.do"
payload = {
    "rep": "1",
    "key": "1",
    "manageCode": "",
    "searchKrwd": "파이썬"
}

try:
    r = session.post(url, data=payload, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("gimpo_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved gimpo_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 총 건수 및 결과 목록
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    titles = soup.select(".bookArea a.book_name, a.book_name, .title a, a[href*='Detail'], .book_list a, a[href*='bookSearchDetail']")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()}")
        
    print("Keyword count:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
