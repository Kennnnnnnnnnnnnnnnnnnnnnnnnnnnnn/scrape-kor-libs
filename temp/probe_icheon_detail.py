"""
이천시도서관 상세페이지(search/detail/) 기반 청구기호/소장처 검증
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
    'Referer': 'https://www.icheonlib.go.kr/search/tot/result?q=%ED%8C%8C%EC%9D%B4%EC%8D%AC'
}

url = "https://www.icheonlib.go.kr/search/detail/CATTOT000001105601"

try:
    r = session.get(url, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("icheon_detail.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved icheon_detail.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 1. 소장 정보 테이블 탐색
    print("\n=== 소장 정보 테이블 탐색 ===")
    tables = soup.select("table")
    print(f"Tables found: {len(tables)}")
    for i, table in enumerate(tables):
        headers = [th.text.strip() for th in table.select("th")]
        print(f"  Table[{i}] Headers: {headers}")
        rows = table.select("tbody tr")
        print(f"    Rows count: {len(rows)}")
        for r_idx, row in enumerate(rows[:5]):
            cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
            print(f"      Row[{r_idx}]: {cols}")
except Exception as e:
    print("Error:", e)
