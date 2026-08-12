"""
수원시 모바일 통합검색 API 실시간 호출 검증
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import json

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

s = requests.Session()
s.mount('https://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://mob.suwonlib.go.kr/getSearchResult/BOOK"

# searchNew260211.js 분석 기준 기본 파라미터 셋
payload = {
    "searchTxt": "파이썬",
    "searchKind": "SIMPLE",
    "manageCode": "",  # 빈 값 또는 ALL
    "isInnerSearch": "F",
    "innerSearchTxt": "",
    "keywordSearch": "false",
    "displayNo": "10",
    "orderbyItem": "SCORE",
    "orderby": "ASC",
    "pageNo": "1",
    "kCid": "",
    "kdcValue": ""
}

try:
    # xhr.setRequestHeader("ajax", true); 가 js에 있었으므로 X-Requested-With 나 ajax 헤더 추가
    headers = HEADERS.copy()
    headers["ajax"] = "true"
    headers["X-Requested-With"] = "XMLHttpRequest"
    
    r = s.post(url, data=payload, headers=headers, verify=False, timeout=10)
    print("Status:", r.status_code)
    print("Response Length:", len(r.text))
    
    data = r.json()
    print("\n=== JSON KEY STRUCTURE ===")
    print(list(data.keys()))
    
    if "SEARCH_RESULT" in data:
        res = data["SEARCH_RESULT"]
        print(f"SEARCH_COUNT: {res.get('SEARCH_COUNT')}")
        book_list = res.get("SEARCH_LIST", [])
        print(f"Items count: {len(book_list)}")
        if book_list:
            print("\n=== FIRST BOOK DETAIL ===")
            print(json.dumps(book_list[0], ensure_ascii=False, indent=2))
except Exception as e:
    print("Error:", e)
