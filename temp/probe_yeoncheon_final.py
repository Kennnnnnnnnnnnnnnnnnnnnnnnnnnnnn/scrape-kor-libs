"""
연천군도서관 진짜 파라미터 조합 GET 통합검색 최종 실시간 검증
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
    'Referer': 'https://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do'
}

url = "https://library.yeoncheon.go.kr/menu/10039/program/30005/searchResultList.do"

# 다중 지점코드와 searchLibrary, searchKeyword 최종 조립
params = [
    ("searchLibraryArr", "MA"),
    ("searchLibraryArr", "BR"),
    ("searchLibraryArr", "ME"),
    ("searchLibraryArr", "MD"),
    ("searchLibraryArr", "MF"),
    ("searchLibraryArr", "MG"),
    ("searchLibrary", "ALL"),  # searchLibrary 명시!
    ("searchKeyword", "파이썬"),
    ("searchType", "SIMPLE"),
    ("searchKey", "ALL")
]

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("yeoncheon_real_library_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved yeoncheon_real_library_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 목록 파싱
    book_items = soup.select("dl.bookDataWrap")
    print(f"Book items count: {len(book_items)}")
    
    for i, item in enumerate(book_items[:6]):
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
