"""
하남시도서관 검색어 EUC-KR 수동 인코딩 검색 실시간 검증
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
session.mount('https://', SslAdapter())
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.hanamlib.go.kr/nalib/index.do'
}

# 1. "파이썬" 단어를 EUC-KR로 수동 인코딩
kwd_euckr = "파이썬".encode("euc-kr")
kwd_enc = urllib.parse.quote(kwd_euckr)
print(f"EUC-KR Encoded '파이썬': {kwd_enc}")

url = f"https://www.hanamlib.go.kr/kolaseek/search/plusSearchResultList.do?searchLibraryArr=&searchKeyword={kwd_enc}&searchType=SIMPLE&searchCategory=ALL&searchKey=ALL"

try:
    r = session.get(url, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("hanam_real_euckr_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved hanam_real_euckr_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 총 검색 건수 노출 단락 탐색
    cnt_tag = soup.select_one("strong.searcKwd ~ span.themeFC, strong.searcKwd ~ b.themeFC")
    if not cnt_tag:
        cnt_tag = soup.select_one("span.themeFC")
    print("Result Count Text:", cnt_tag.text.strip() if cnt_tag else "None")
    
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    # 파주시와 동일한 JSP/KOLAS 디자인이므로 dl.bookDataWrap, dt.tit a 사용
    book_items = soup.select("dl.bookDataWrap")
    print(f"Book items: {len(book_items)}")
    for i, item in enumerate(book_items[:5]):
        title_tag = item.select_one("dt.tit a")
        title = title_tag.text.strip() if title_tag else "None"
        author_tag = item.select_one("dd.author span")
        author = author_tag.text.strip() if author_tag else "None"
        call_tag = item.select_one("dd.data span")
        call_no = call_tag.text.strip() if call_tag else "None"
        print(f"  [{i}] Title: {title} | Author: {author} | CallNo: {call_no}")
        
except Exception as e:
    print("Error:", e)
