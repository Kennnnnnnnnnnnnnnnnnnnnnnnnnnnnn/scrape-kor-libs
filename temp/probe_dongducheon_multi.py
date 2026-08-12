"""
동두천시 관내 모든 지점 코드들을 동봉한 통합 검색 실시간 검증
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
    'Referer': 'https://lib.ddc.go.kr/kolaseek/plus/search/plusSearchSimple.do?searchLibrary=ALL'
}

url = "https://lib.ddc.go.kr/kolaseek/plus/search/plusSearchResultList.do"

# 다중 지점코드 대입!
params = [
    ("searchLibraryArr", "MA"),
    ("searchLibraryArr", "MC"),
    ("searchLibraryArr", "MB"),
    ("searchLibraryArr", "SB"),
    ("searchLibraryArr", "SE"),
    ("searchKeyword", "파이썬"),
    ("searchType", "SIMPLE"),
    ("searchCategory", "ALL"),
    ("searchKey", "ALL")
]

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    book_items = soup.select("dl.bookDataWrap")
    print(f"Book items count: {len(book_items)}")
    
    for i, item in enumerate(book_items[:8]):
        title_tag = item.select_one("dt.tit a")
        title = title_tag.text.strip() if title_tag else "None"
        title = re.sub(r"^\d+\.\s*", "", title)
        
        author_tag = item.select_one("dd.author span")
        author = author_tag.text.strip() if author_tag else "None"
        author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", author)
        
        # 청구기호 추출
        call_no = ""
        data_spans = item.select("dd.data span")
        for span in data_spans:
            txt = span.text.strip()
            if "청구기호" in txt:
                call_no = txt.replace("청구기호", "").replace(":", "").replace("위치", "").strip()
                call_no = re.sub(r"\s+", " ", call_no).strip()
                break
                
        # 도서관명 추출
        lib_name = ""
        site_spans = item.select("dd.site span")
        for span in site_spans:
            txt = span.text.strip()
            if "관:" in txt or "도서관" in txt or "관 " in txt:
                lib_name = txt.replace("관", "").replace(":", "").strip()
                lib_name = re.sub(r"\s+", " ", lib_name).strip()
                break
                
        print(f"  [{i}] [{lib_name}] {title[:40]} | Author: {author[:20]} | CallNo: {call_no}")
        
except Exception as e:
    print("Error:", e)
