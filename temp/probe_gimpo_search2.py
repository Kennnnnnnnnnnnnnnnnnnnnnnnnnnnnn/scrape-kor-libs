"""
김포시도서관 통합검색(modam/bookSearchList.do) POST 진짜 검증
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

# 통합 검색 액션
url = "https://www.gimpo.go.kr/modam/bookSearchList.do?allCheck=ALL"
payload = {
    "rep": "1",
    "key": "11488",
    "manageCode": "BR,DK,GC,GR,HS,JG,MA,MS,PM,TJ,YG,YY,MD",
    "searchKrwd": "파이썬"
}

try:
    r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("gimpo_real_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved gimpo_real_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    # 일반적인 리스트 구조 탐색
    titles = soup.select(".title a, a[href*='bookSearchDetail'], a.book_name, .book_list a")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()} | Href: {t.get('href')}")
        
    print("Keyword count:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
