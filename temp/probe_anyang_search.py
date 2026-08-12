"""
안양시도서관 searchResultList.do 실시간 검색 및 청구기호 추출 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import re

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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.anyang.go.kr/intro/searchResultList.do"
params = {
    "searchKeyword": "파이썬",
    "searchType": "SIMPLE",
    "searchManageCode": "ALL",
    "topSearchCondition": "ALL",
    "searchArticle": "SCORE",
    "searchOrder": "ASC"
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    soup = BeautifulSoup(r.text, "html.parser")
    with open("anyang_search.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    # 총 건수 파싱
    total_tag = soup.select_one("#totalCnt")
    total_cnt = total_tag.text.strip() if total_tag else "No totalCnt"
    print("Total Count:", total_cnt)
    
    # 책 제목 목록
    print("\n=== 제목 목록 ===")
    titles = soup.select("a.book_name, .bookArea a.book_name")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
         print(f"  [{i}] Title: {t.text.strip()}")
except Exception as e:
    print("Error:", e)
