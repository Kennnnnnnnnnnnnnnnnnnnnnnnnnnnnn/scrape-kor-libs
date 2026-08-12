"""
양주시도서관 진짜 통합검색 결과 HTML 다운로드 및 파이싱 검증
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.libyj.go.kr/'
}

url = "https://www.libyj.go.kr/ojlake/plusSearchResultList.do"
params = {
    "searchKeyword": "파이썬",
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL"
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 목록
    book_items = soup.select("dl.bookDataWrap")
    print(f"Book items: {len(book_items)}")
    
    for i, item in enumerate(book_items[:6]):
        title_tag = item.select_one("dt.tit a")
        title = title_tag.text.strip() if title_tag else "None"
        title = re.sub(r"^\d+\.\s*", "", title)
        
        author_tag = item.select_one("dd.author span")
        author = author_tag.text.strip() if author_tag else "None"
        author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", author)
        
        # 소장 도서관 및 청구기호 추출
        # dl.bookDataWrap 안의 모든 dd 태그 덤프하여 정확한 지점/청구기호 매핑 규명
        print(f"\n[{i}] Title: {title[:40]} | Author: {author[:20]}")
        for dd in item.select("dd"):
            cls = dd.get("class", [])
            txt = dd.text.strip().replace("\n", " ").replace("\t", " ")
            txt = re.sub(r"\s+", " ", txt)
            print(f"  dd(class={cls}): '{txt}'")
            
except Exception as e:
    print("Error:", e)
