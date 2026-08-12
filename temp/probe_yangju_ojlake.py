"""
양주시도서관 ojlake 서블릿 기반 통합검색 실시간 검증
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
    'Referer': 'https://www.libyj.go.kr/'
}

# 2가지 경로 후보군 교차 테스트
urls = [
    "https://www.libyj.go.kr/ojlake/search/plusSearchResultList.do",
    "https://www.libyj.go.kr/ojlake/plusSearchResultList.do"
]

for url in urls:
    print(f"\n--- Testing URL: {url} ---")
    params = {
        "searchKeyword": "파이썬",
        "searchType": "SIMPLE",
        "searchCategory": "ALL",
        "searchKey": "ALL"
    }
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
        print("  Status:", r.status_code)
        print("  Length:", len(r.text))
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            book_items = soup.select("dl.bookDataWrap")
            print(f"  Book items count: {len(book_items)}")
            
            for i, item in enumerate(book_items[:3]):
                title_tag = item.select_one("dt.tit a")
                title = title_tag.text.strip() if title_tag else "None"
                print(f"    [{i}] Title: {title}")
                
    except Exception as e:
        print("  Error:", e)
