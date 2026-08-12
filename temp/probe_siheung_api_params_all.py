"""
시흥 collections search API 파라미터 조합 검증
"""
import requests
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

col_ids = [1, 2, 3, 4]
queries = ["python", "파이썬"]

for cid in col_ids:
    for q in queries:
        url = f"https://lib.siheung.go.kr/pyxis-api/1/collections/{cid}/search"
        params = {"all": q, "max": "10"}
        try:
            r = session.get(url, params=params, headers=HEADERS, timeout=6, verify=False)
            data = r.json()
            total = data.get("data", {}).get("totalCount", 0) if isinstance(data.get("data"), dict) else 0
            print(f"ColID: {cid}, Query: {q} -> Status: {r.status_code}, Total: {total}, Success: {data.get('success')}, data_type={type(data.get('data'))}")
            if total > 0:
                print("  [SUCCESS] First item title:", data["data"]["list"][0].get("title") or data["data"]["list"][0].get("mainTitle"))
        except Exception as e:
            print(f"ColID: {cid}, Query: {q} -> Error: {e}")
