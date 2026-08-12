"""
연천군도서관 평문 HTTP 프로토콜 및 세션쿠키 유지 최종 결합 실시간 검증
"""
import requests
import urllib.parse
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
session.mount('http://', SslAdapter())
session.mount('https://', SslAdapter())

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'http://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do'
}

try:
    # 1. 메인 세션 획득 (HTTP 평문 활용!)
    print("=== 1. 평문 HTTP 간략검색 페이지 방문 ===")
    r_simple = session.get("http://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do", headers=HEADERS, timeout=8)
    print("  Status:", r_simple.status_code)
    print("  Cookies:", session.cookies.get_dict())
    
    # 2. UTF-8 인코딩 검색
    print("\n=== 2. UTF-8 + 지점코드 검색 ===")
    url_utf8 = "http://library.yeoncheon.go.kr/menu/10039/program/30005/searchResultList.do"
    params_utf8 = [
        ("searchLibraryArr", "MA"),
        ("searchLibraryArr", "BR"),
        ("searchLibraryArr", "ME"),
        ("searchLibraryArr", "MD"),
        ("searchLibraryArr", "MF"),
        ("searchLibraryArr", "MG"),
        ("searchLibrary", "ALL"),
        ("searchKeyword", "파이썬"),
        ("searchType", "SIMPLE"),
        ("searchKey", "ALL")
    ]
    
    r_utf8 = session.get(url_utf8, params=params_utf8, headers=HEADERS, timeout=10)
    print("  UTF8 HTML Length:", len(r_utf8.text))
    
    # 3. EUC-KR 인코딩 검색
    print("\n=== 3. EUC-KR + 지점코드 검색 ===")
    kwd_euckr = "파이썬".encode("euc-kr")
    kwd_enc = urllib.parse.quote(kwd_euckr)
    query_str = f"searchLibraryArr=MA&searchLibraryArr=BR&searchLibraryArr=ME&searchLibraryArr=MD&searchLibraryArr=MF&searchLibraryArr=MG&searchLibrary=ALL&searchKeyword={kwd_enc}&searchType=SIMPLE&searchKey=ALL"
    url_euckr = f"{url_utf8}?{query_str}"
    
    r_euckr = session.get(url_euckr, headers=HEADERS, timeout=10)
    print("  EUCKR HTML Length:", len(r_euckr.text))
    
    if len(r_utf8.text) > 1000:
        soup = BeautifulSoup(r_utf8.text, "html.parser")
        book_items = soup.select("dl.bookDataWrap")
        print(f"  Book items in UTF8: {len(book_items)}")
        
    if len(r_euckr.text) > 1000:
        soup = BeautifulSoup(r_euckr.text, "html.parser")
        book_items = soup.select("dl.bookDataWrap")
        print(f"  Book items in EUCKR: {len(book_items)}")
        for i, item in enumerate(book_items[:3]):
            title = item.select_one("dt.tit a").text.strip()
            print(f"    [{i}] Title: {title}")
            
except Exception as e:
    print("Error:", e)
