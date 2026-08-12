"""
군포시도서관 Pyxis API 인코딩 강제 우회 및 영어 1/3 컬렉션 정밀 검증
"""
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

# 1번 컬렉션, 3번 컬렉션
colls = ["1", "3"]

for col in colls:
    url = f"https://www.gunpolib.go.kr/pyxis-api/1/collections/{col}/search"
    print(f"\n=== Collection {col} Testing ===")
    
    # 1. 영어 'python'
    try:
        params = {"all": "kwd:python", "max": 10, "start": 0}
        r = requests.get(url, params=params, headers=HEADERS, timeout=6, verify=False)
        data = r.json()
        total = data.get("data", {}).get("totalCount", 0) if data.get("data") else 0
        print(f"  English 'python' -> Total: {total} (Success: {data.get('success')})")
    except Exception as e:
        print("  English Error:", e)
        
    # 2. 한글 수동 quote '파이썬'
    try:
        # requests가 이중인코딩하지 않도록 문자열이 아닌 수동 조립 URL로 통신!
        kwd_enc = urllib.parse.quote("파이썬")
        final_url = f"{url}?all=kwd:{kwd_enc}&max=10&start=0"
        
        r = requests.get(final_url, headers=HEADERS, timeout=6, verify=False)
        data = r.json()
        total = data.get("data", {}).get("totalCount", 0) if data.get("data") else 0
        print(f"  Manual Encoded '파이썬' -> Total: {total} (Success: {data.get('success')})")
        if total > 0:
            list_data = data.get("data", {}).get("list", [])
            for i, item in enumerate(list_data[:2]):
                print(f"    [{i}] Title: {item.get('title')} / Author: {item.get('author')}")
    except Exception as e:
        print("  Korean Error:", e)
