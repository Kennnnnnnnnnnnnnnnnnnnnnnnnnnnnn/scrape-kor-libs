import requests, urllib3, json
urllib3.disable_warnings()

url = "https://www.nowonlib.kr/api/search"
payload = {
    "searchKeyword": "파친코",
    "page": 1,
    "display": 20
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.nowonlib.kr/'
}

r = requests.post(url, json=payload, headers=headers, timeout=12, verify=False)
data = r.json()

print("Status:", r.status_code)
contents = data.get("contents", {})
print("TotalCount:", contents.get("totalCount"))
items = contents.get("bookList", [])
print(f"Items returned: {len(items)}\n")

if items:
    print("Keys of first item:", list(items[0].keys()))
    print("\nFirst item detail:")
    print(json.dumps(items[0], ensure_ascii=False, indent=2))
    
    print("\nCall numbers for all items:")
    for idx, it in enumerate(items, 1):
        print(f" #{idx} | Title: {it.get('title')} | libName: {it.get('libName')} | callNo: {it.get('callNo')} | call_no: {it.get('call_no')} | callNo1: {it.get('callNo1')} | shelfLocName: {it.get('shelfLocName')}")
