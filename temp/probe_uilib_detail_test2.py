"""
의정부시 도서관 다른 도서 상세페이지 소장 테이블 검증
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
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 1. Match 5 책 (ISBN: 8989345588)
# 2. Match 7 책 (ISBN: 9788970506562)
tests = [
    {"menu_idx": "9", "isbn": "8989345588", "speciesKey": "1157102", "booktype": "MO"},
    {"menu_idx": "9", "isbn": "9788970506562", "speciesKey": "1668989", "booktype": "MO"}
]

for idx, params in enumerate(tests):
    print(f"\n--- Test[{idx}] params: {params} ---")
    try:
        r = session.get("https://www.uilib.go.kr/main/intro/search/detail.do", params=params, headers=HEADERS, timeout=8, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        
        tables = soup.select("table")
        print(f"  Tables: {len(tables)}")
        for t_idx, table in enumerate(tables):
            headers = [th.text.strip() for th in table.select("th")]
            rows = table.select("tbody tr")
            if "도서관" in "".join(headers) or "청구기호" in "".join(headers):
                print(f"    Table[{t_idx}] (Headers: {headers}) -> Rows: {len(rows)}")
                for r_idx, row in enumerate(rows[:5]):
                    cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
                    print(f"      Row[{r_idx}]: {cols}")
    except Exception as e:
        print("  Error:", e)
