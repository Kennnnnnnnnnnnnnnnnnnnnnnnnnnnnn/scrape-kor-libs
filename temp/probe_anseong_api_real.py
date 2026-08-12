"""
안성시 biblioSearch.do JSON API 검증
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.anseong.go.kr/library/search/biblioSearch.do"
payload = {
    "biblioId": 884824,
    "branchId": 8
}

r = session.post(url, data=payload, headers=HEADERS, timeout=8, verify=False)
print("Status:", r.status_code)
print("Response text:", r.text[:300])

data = json.loads(r.text)
if data.get("success"):
    items = data.get("data", {}).get("list", [])
    print(f"Items count: {len(items)}")
    for item in items:
        loc = item.get("location", {}).get("name", "")
        callNo = item.get("callNo", "")
        state = item.get("itemState", {}).get("name", "")
        circState = item.get("circulationState", {}).get("name", "") if item.get("circulationState") else ""
        print(f"  Barcode: {item.get('barcode')} | Loc: {loc} | CallNo: {callNo} | State: {state}/{circState}")
