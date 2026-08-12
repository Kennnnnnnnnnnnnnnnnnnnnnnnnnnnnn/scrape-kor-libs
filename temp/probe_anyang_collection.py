"""
안양시립도서관 소장 정보(collectionBookList.do) XHR 요청 및 청구기호 분석
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
    'Referer': 'https://lib.anyang.go.kr/intro/searchResultList.do',
    'X-Requested-With': 'XMLHttpRequest'
}

url = "https://lib.anyang.go.kr/search/include/collectionBookList.do"
payload = {
    "speciesKey": "20156253,20156256,20156258,20156261",
    "pubFormCode": "MO"
}

try:
    r = session.post(url, data=payload, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    soup = BeautifulSoup(r.text, "html.parser")
    with open("anyang_collection.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    # 테이블 구조 분석
    # 청구기호 컬럼의 값을 찾음 (보통 th에 '청구기호'가 있고 td 매칭)
    table = soup.select_one("table")
    if table:
        print("\n=== 소장 정보 테이블 발견 ===")
        headers = [th.text.strip() for th in table.select("th")]
        print("Table Headers:", headers)
        
        rows = table.select("tbody > tr")
        print(f"Total Rows: {len(rows)}")
        for i, row in enumerate(rows[:5]):
            cols = [td.text.strip() for td in row.select("td")]
            print(f"  Row[{i}]: {cols}")
    else:
        print("Table not found in HTML fragment")
except Exception as e:
    print("Error:", e)
