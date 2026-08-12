"""
안성시도서관 세션 유지 후 상세페이지(searchView.do) POST/GET 최종 검증
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
    'Referer': 'https://www.anseong.go.kr/library/contents.do?mId=0101010000'
}

# 1. 1차 통합검색 수행하여 진짜 biblioId 수집
search_url = "https://www.anseong.go.kr/library/search/search.do"
params = {
    "mId": "0101010100",
    "searchKeyType": "K",
    "page": "1",
    "searchType": "ALL",
    "searchTxt": "파이썬",
    "branchId": ""
}

try:
    print("=== 1. 1차 검색 수행 ===")
    r_search = session.get(search_url, params=params, headers=HEADERS, timeout=10, verify=False)
    soup = BeautifulSoup(r_search.text, "html.parser")
    
    # 2. 결과 HTML 에서 진짜 goView 인자(biblioId) 추출
    html_text = r_search.text
    matches = re.findall(r"goView\((\d+)(?:\.\d+)?\)", html_text)
    print("  Real biblioIds found:", matches)
    
    if matches:
        real_id = matches[0]
        print(f"  Target biblioId: {real_id}")
        
        # 3. 세션을 그대로 들고 상세페이지 GET 요청!
        detail_url = "https://www.anseong.go.kr/library/search/searchView.do"
        d_params = {
            "mId": "0101010100",
            "biblioId": real_id
        }
        
        print(f"\n=== 2. 상세페이지 GET 요청: {d_params} ===")
        r_get = session.get(detail_url, params=d_params, headers=HEADERS, timeout=8, verify=False)
        print("  GET Status:", r_get.status_code)
        
        # 4. 세션을 그대로 들고 상세페이지 POST 요청!
        print(f"\n=== 3. 상세페이지 POST 요청 ===")
        r_post = session.post(detail_url, data=d_params, headers=HEADERS, timeout=8, verify=False)
        print("  POST Status:", r_post.status_code)
        print("  POST HTML Length:", len(r_post.text))
        
        # 소장처 테이블 덤프
        dsoup = BeautifulSoup(r_post.text, "html.parser")
        tables = dsoup.select("table")
        print(f"  Tables found: {len(tables)}")
        for t_idx, table in enumerate(tables):
            headers = [th.text.strip() for th in table.select("th")]
            if any(h in "".join(headers) for h in ["도서관", "청구", "번호", "소장"]):
                rows = table.select("tbody tr")
                print(f"    Table[{t_idx}] (Headers: {headers}) -> Rows: {len(rows)}")
                for r_idx, row in enumerate(rows[:5]):
                    cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
                    print(f"      Row[{r_idx}]: {cols}")
except Exception as e:
    print("Error:", e)
