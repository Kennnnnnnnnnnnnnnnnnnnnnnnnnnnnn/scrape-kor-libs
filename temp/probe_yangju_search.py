"""
양주시도서관 진짜 검색 서블릿(plusSearchResultList.do) GET 실시간 검증
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

url = "https://www.libyj.go.kr/kolaseek/search/plusSearchResultList.do"
params = {
    "searchLibraryArr": "",  # 전체 지점 대상
    "searchKeyword": "파이썬",
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL"
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("yangju_real_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved yangju_real_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 제목 태그 분석 (dl.bookDataWrap, dt.tit a)
    book_items = soup.select("dl.bookDataWrap")
    print(f"Book items count: {len(book_items)}")
    for i, item in enumerate(book_items[:5]):
        title_tag = item.select_one("dt.tit a")
        title = title_tag.text.strip() if title_tag else "None"
        author_tag = item.select_one("dd.author span")
        author = author_tag.text.strip() if author_tag else "None"
        
        # 청구기호 추출
        call_no = ""
        data_spans = item.select("dd.data span")
        for span in data_spans:
            txt = span.text.strip()
            if "청구기호" in txt:
                call_no = txt.replace("청구기호", "").replace(":", "").replace("위치", "").strip()
                break
                
        # 도서관명 추출
        lib_name = ""
        site_spans = item.select("dd.site span")
        for span in site_spans:
            txt = span.text.strip()
            if "관:" in txt or "도서관" in txt or "관 " in txt:
                lib_name = txt.replace("관", "").replace(":", "").strip()
                break
                
        print(f"  [{i}] [{lib_name}] {title} | Author: {author} | CallNo: {call_no}")
        
except Exception as e:
    print("Error:", e)
