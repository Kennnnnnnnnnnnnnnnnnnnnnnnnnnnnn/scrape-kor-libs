"""
안산시도서관 /api/search API 실시간 호출 검증
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import json

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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "http://lib.iansan.net/api/search"
params = {
    "searchKeyword": "파이썬",
    "page": "1",
    "display": "10"
}

# GET 방식 테스트
print("=== 1. GET Request ===")
try:
    r = session.get(url, params=params, headers=HEADERS, timeout=8)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    if r.status_code == 200:
        data = r.json()
        print("Keys:", list(data.keys()))
        if "contents" in data:
            contents = data["contents"]
            print("Total Count:", contents.get("totalCount", 0))
            book_list = contents.get("bookList", []) or contents.get("list", [])
            print(f"Book items: {len(book_list)}")
            if book_list:
                print("First Book:", json.dumps(book_list[0], ensure_ascii=False, indent=2))
except Exception as e:
    print("GET Error:", e)

# POST (JSON) 방식 테스트
print("\n=== 2. POST (JSON) Request ===")
try:
    r = session.post(url, json=params, headers=HEADERS, timeout=8)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    if r.status_code == 200:
        data = r.json()
        print("Keys:", list(data.keys()))
        if "contents" in data:
            contents = data["contents"]
            print("Total Count:", contents.get("totalCount", 0))
            book_list = contents.get("bookList", []) or contents.get("list", [])
            print(f"Book items: {len(book_list)}")
            if book_list:
                print("First Book:", json.dumps(book_list[0], ensure_ascii=False, indent=2))
except Exception as e:
    print("POST Error:", e)
