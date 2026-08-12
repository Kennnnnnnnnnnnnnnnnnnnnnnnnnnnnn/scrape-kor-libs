"""
노원구립도서관 (www.nowonlib.kr/api/search) REST API 검증
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.nowonlib.kr/'
}

url = "https://www.nowonlib.kr/api/search"
payload = {
    "searchKeyword": "파이썬",
    "page": 1,
    "display": 5
}

r = session.post(url, json=payload, headers=HEADERS, timeout=10, verify=False)
print("Status:", r.status_code, "Len:", len(r.text))

if r.status_code == 200:
    data = r.json()
    contents = data.get("contents", {})
    print("Total count:", contents.get("totalCount"))
    items = contents.get("bookList", [])
    print(f"Items count: {len(items)}")

    for i, item in enumerate(items):
        print(f"\n=== Item [{i+1}] ===")
        print("  title:", item.get("title") or item.get("originalTitle"))
        print("  author:", item.get("author") or item.get("originalAuthor"))
        print("  callNo:", item.get("callNo"))
        print("  libName:", item.get("libName"))
        print("  shelfLocName:", item.get("shelfLocName"))
