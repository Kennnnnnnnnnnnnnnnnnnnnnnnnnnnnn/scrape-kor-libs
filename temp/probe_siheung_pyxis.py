"""
시흥시도서관 Pyxis API 실시간 연동 검증
"""
import requests
import json
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
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://lib.siheung.go.kr/'
}

# collection 1 (도서) 과 3 (전체) 교차 검증
col_ids = [1, 3]

for cid in col_ids:
    url = f"https://lib.siheung.go.kr/pyxis-api/1/collections/{cid}/search"
    params = {
        "all": "1|k|a|파이썬",
        "max": "20",
        "start": "1"
    }
    
    print(f"\n--- Testing Pyxis Collection {cid} ---")
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        print("  Status:", r.status_code)
        
        if r.status_code == 200:
            data = r.json()
            with open(f"siheung_pyxis_{cid}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Saved siheung_pyxis_{cid}.json")
            
            # 검색 결과 수집 카운트 출력
            total = data.get("data", {}).get("totalCount", 0)
            list_data = data.get("data", {}).get("list", [])
            print(f"  Total count: {total} | List size: {len(list_data)}")
            
            for i, item in enumerate(list_data[:3]):
                title = item.get("titleStatement", "None")
                author = item.get("author", "None")
                bid = item.get("id", "None")
                print(f"    [{i}] ID: {bid} | Title: {title} | Author: {author}")
                
    except Exception as e:
        print("  Error:", e)
