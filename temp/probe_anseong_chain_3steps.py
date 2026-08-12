"""
안성시도서관 3단계 세션 체인 완벽 상세 검증
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
    'Referer': 'https://www.anseong.go.kr/library/main.do'
}

try:
    # Step 1: 메인 도메인 방문 (세션 쿠키 생성)
    print("=== Step 1. 메인 홈페이지 방문 ===")
    r_main = session.get("https://www.anseong.go.kr/library/main.do", headers=HEADERS, timeout=8, verify=False)
    print("  Status:", r_main.status_code)
    print("  Cookies:", session.cookies.get_dict())
    
    # Step 2: 1차 검색 수행
    print("\n=== Step 2. 1차 통합 검색 수행 ===")
    search_url = "https://www.anseong.go.kr/library/search/search.do"
    params = {
        "mId": "0101010100",
        "searchKeyType": "K",
        "page": "1",
        "searchType": "ALL",
        "searchTxt": "파이썬",
        "branchId": ""
    }
    r_search = session.get(search_url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("  Search Status:", r_search.status_code)
    print("  Cookies:", session.cookies.get_dict())
    
    # Step 3: 수집한 쿠키 세션으로 진짜 상세페이지 찌르기!
    print("\n=== Step 3. 상세페이지 GET 요청 ===")
    detail_url = "https://www.anseong.go.kr/library/search/searchView.do"
    d_params = {
        "mId": "0101010100",
        "biblioId": "238934"  # 파이썬 책 ID 예시
    }
    
    r_detail = session.get(detail_url, params=d_params, headers=HEADERS, timeout=10, verify=False)
    print("  Detail Status:", r_detail.status_code)
    print("  Detail HTML Length:", len(r_detail.text))
    
    with open("anseong_detail_chain.html", "w", encoding="utf-8") as f:
        f.write(r_detail.text)
    print("  Saved anseong_detail_chain.html")
    
    soup = BeautifulSoup(r_detail.text, "html.parser")
    tables = soup.select("table")
    print(f"  Tables found: {len(tables)}")
    for i, table in enumerate(tables):
        headers = [th.text.strip() for th in table.select("th")]
        if any(h in "".join(headers) for h in ["도서관", "청구", "번호", "소장"]):
            print(f"    Table[{i}] Headers: {headers}")
            rows = table.select("tbody tr")
            print(f"      Rows count: {len(rows)}")
            for r_idx, row in enumerate(rows[:5]):
                cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
                print(f"        Row[{r_idx}]: {cols}")
except Exception as e:
    print("Error:", e)
