"""
시흥시도서관 백엔드 collections search API 호출 실시간 검증
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

# collections/1/search API 호출
url = "https://lib.siheung.go.kr/pyxis-api/1/collections/1/search"
params = {
    "all": "파이썬",
    "max": "10",
    "offset": "0",
    "sort": "RANK",
    "order": "DESC"
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status Code:", r.status_code)
    print("Response Length:", len(r.text))
    data = r.json()
    print("\n=== JSON KEY STRUCTURE ===")
    print(list(data.keys()))
    
    if "success" in data and data["success"]:
        res_data = data.get("data", {})
        print("Total Count:", res_data.get("totalCount", 0))
        list_data = res_data.get("list", [])
        print(f"List items: {len(list_data)}")
        if list_data:
            print("\n=== FIRST ITEM DETAILS ===")
            print(json.dumps(list_data[0], ensure_ascii=False, indent=2))
    else:
        print("Fail response:", data)
except Exception as e:
    print("Error:", e)
