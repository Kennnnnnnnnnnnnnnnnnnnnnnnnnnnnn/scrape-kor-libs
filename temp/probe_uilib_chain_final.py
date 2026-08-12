"""
의정부시 도서관 bookkey 파라미터를 추가한 상세 소장처 테이블 최종 검증
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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

# 1. 1차 통합검색 수행
search_url = "https://www.uilib.go.kr/main/intro/search/index.do"
search_params = {
    "menu_idx": "9",
    "booktype": "ALL",
    "title": "파이썬"
}

try:
    r_search = session.get(search_url, params=search_params, headers=HEADERS, timeout=10, verify=False)
    soup = BeautifulSoup(r_search.text, "html.parser")
    items = soup.select(".item")
    
    for idx, item in enumerate(items[:3]):
        detail_link = item.select_one("a.name, a.goDetail")
        if not detail_link:
            continue
        href = detail_link.get("href", "")
        
        # bookkey 파라미터까지 전부 파싱!
        m_isbn = re.search(r"isbn=([^&]+)", href)
        m_sp = re.search(r"speciesKey=([^&]+)", href)
        m_bk = re.search(r"bookkey=([^&]+)", href)
        m_bt = re.search(r"booktype=([^&]+)", href)
        
        if m_isbn and m_sp and m_bk:
            isbn = m_isbn.group(1).strip()
            species_key = m_sp.group(1).strip()
            book_key = m_bk.group(1).strip()
            booktype = m_bt.group(1).strip() if m_bt else "MO"
            
            # 2. 모든 필수 키들을 고스란히 들고 상세 페이지 찌르기!
            detail_url = "https://www.uilib.go.kr/main/intro/search/detail.do"
            d_params = {
                "menu_idx": "9",
                "isbn": isbn,
                "speciesKey": species_key,
                "bookkey": book_key,
                "booktype": booktype
            }
            
            print(f"\n--- 2차 상세페이지 요청 [Book {idx}]: {d_params} ---")
            r_detail = session.get(detail_url, params=d_params, headers=HEADERS, timeout=8, verify=False)
            dsoup = BeautifulSoup(r_detail.text, "html.parser")
            
            tables = dsoup.select("table")
            print(f"  Tables found: {len(tables)}")
            for t_idx, table in enumerate(tables):
                headers = [th.text.strip() for th in table.select("th")]
                if "도서관" in "".join(headers) or "청구기호" in "".join(headers):
                    rows = table.select("tbody tr")
                    print(f"    Table[{t_idx}] (Headers: {headers}) -> Rows: {len(rows)}")
                    for r_idx, row in enumerate(rows[:5]):
                        cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
                        print(f"      Row[{r_idx}]: {cols}")
except Exception as e:
    print("Error:", e)
