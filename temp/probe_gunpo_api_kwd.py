"""
군포시도서관 Pyxis API kwd 접두사 검색 검증
"""
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

url = "https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search"

# Pyxis API 고유의 kwd: 접두사 쿼리 파라미터 세팅!
params_sets = [
    {
        "all": "kwd:파이썬",
        "max": 10,
        "start": 0,
        "searchField": "ALL"
    },
    {
        "q": "파이썬",
        "all": "kwd:파이썬",
        "searchKeyword": "파이썬",
        "max": 10
    }
]

for idx, params in enumerate(params_sets):
    print(f"\n--- Params[{idx}]: {params} ---")
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200:
            data = r.json()
            print("  Success:", data.get("success"))
            print("  Code:", data.get("code"))
            total = data.get("data", {}).get("totalCount", 0) if data.get("data") else 0
            print("  TotalCount:", total)
            
            # 검색 도서 목록 일부 덤프
            list_data = data.get("data", {}).get("list", []) if data.get("data") else []
            print(f"  Returned list items: {len(list_data)}")
            for i, item in enumerate(list_data[:3]):
                print(f"    [{i}] Title: {item.get('title')} | Author: {item.get('author')}")
    except Exception as e:
        print("  Error:", e)
