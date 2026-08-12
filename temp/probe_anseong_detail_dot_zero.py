"""
안성시도서관 상세페이지 소수점 biblioId(238934.0) 실시간 검증
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
    'Referer': 'https://www.anseong.go.kr/library/search/search.do'
}

# 1. 1차 메인 방문
session.get("https://www.anseong.go.kr/library/main.do", headers=HEADERS, timeout=8, verify=False)

# 2. 1차 검색 방문
search_url = "https://www.anseong.go.kr/library/search/search.do"
params = {
    "mId": "0101010100",
    "searchKeyType": "K",
    "page": "1",
    "searchType": "ALL",
    "searchTxt": "파이썬",
    "branchId": ""
}
session.get(search_url, params=params, headers=HEADERS, timeout=10, verify=False)

# 3. 소수점 .0 이 붙은 biblioId 상세페이지 찌르기!
url = "https://www.anseong.go.kr/library/search/searchView.do"
d_params = {
    "mId": "0101010100",
    "biblioId": "238934.0"  # 소수점 .0 명시!
}

try:
    r = session.get(url, params=d_params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("anseong_detail_dot_zero.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved anseong_detail_dot_zero.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.select("table")
    print(f"Tables found: {len(tables)}")
    for i, table in enumerate(tables):
        headers = [th.text.strip() for th in table.select("th")]
        if any(h in "".join(headers) for h in ["도서관", "청구", "번호", "소장"]):
            print(f"  Table[{i}] (Headers: {headers})")
            rows = table.select("tbody tr")
            print(f"    Rows count: {len(rows)}")
            for r_idx, row in enumerate(rows[:5]):
                cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
                print(f"      Row[{r_idx}]: {cols}")
except Exception as e:
    print("Error:", e)
