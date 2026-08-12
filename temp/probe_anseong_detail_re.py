"""
안성시도서관 이전 쿼리 동봉 상세페이지(searchView.do) 재검증
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

url = "https://www.anseong.go.kr/library/search/searchView.do"
params = {
    "mId": "0101010100",
    "biblioId": "845044",
    "searchKeyType": "K",
    "page": "1",
    "searchType": "ALL",
    "searchTxt": "파이썬",
    "branchId": ""
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("anseong_detail_re.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved anseong_detail_re.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 소장 정보 테이블 탐색
    tables = soup.select("table")
    print(f"Tables found: {len(tables)}")
    for i, table in enumerate(tables):
        headers = [th.text.strip() for th in table.select("th")]
        # 소장 도서관 및 청구기호 컬럼 유무 확인
        if any(h in "".join(headers) for h in ["소장", "도서관", "청구", "번호"]):
            print(f"  Table[{i}] (Headers: {headers})")
            rows = table.select("tbody tr")
            print(f"    Rows count: {len(rows)}")
            for r_idx, row in enumerate(rows[:6]):
                cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
                print(f"      Row[{r_idx}]: {cols}")
except Exception as e:
    print("Error:", e)
