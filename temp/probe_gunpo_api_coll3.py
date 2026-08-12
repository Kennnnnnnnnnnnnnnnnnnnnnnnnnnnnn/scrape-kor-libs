"""
군포시 Pyxis API collection ID 및 키워드 Fuzzing
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.gunpolib.go.kr/'
}

session.get("https://www.gunpolib.go.kr/", headers={'User-Agent': HEADERS['User-Agent']}, verify=False)

print("=== Testing Collections 1~10 with all=1&kwd=python ===")
for cid in range(1, 11):
    url = f"https://www.gunpolib.go.kr/pyxis-api/1/collections/{cid}/search"
    params = {"all": "1", "kwd": "python", "max": 10}
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=5, verify=False)
        print(f"Collection [{cid}] -> Status: {r.status_code}, Len: {len(r.text)}")
        if r.status_code == 200 and "noRecord" not in r.text:
            print(f"  ★ FOUND IN COLLECTION {cid} ★:", r.text[:300])
    except Exception as e:
        print(f"Collection [{cid}] Error: {e}")
