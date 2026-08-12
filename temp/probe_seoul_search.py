"""
강북구립도서관, 강동구립도서관 검색 API 탐색
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 강북구립도서관 (www.gblib.or.kr)
print("=== 강북구립도서관 (gblib.or.kr) ===")
r = session.get("https://www.gblib.or.kr/", headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")
for a in soup.select("a"):
    href = a.get("href", "")
    if "search" in href.lower() or "book" in href.lower():
        txt = a.text.strip()
        if len(txt) > 0 and len(txt) < 30:
            print(f"  '{txt}' -> {href}")

# 강동구립도서관 (gdlibrary.or.kr)
print("\n=== 강동구립도서관 (gdlibrary.or.kr) ===")
# 포털 기반 - API 시도
api_urls = [
    "https://www.gdlibrary.or.kr/portal/api/book/search",
    "https://www.gdlibrary.or.kr/portal/api/v1/book/search",
    "https://www.gdlibrary.or.kr/portal/book/search.json",
]
for url in api_urls:
    try:
        r = session.get(url, params={"keyword": "파이썬", "page": 1, "size": 10},
                       headers={**HEADERS, 'Accept': 'application/json'}, timeout=5, verify=False)
        print(f"  {url.split('portal/')[-1]}: Status: {r.status_code}, CT: {r.headers.get('content-type','')[:30]}, Len: {len(r.text)}")
        if r.status_code == 200 and "파이썬" in r.text:
            print(f"    ★ MATCH! ★ count: {r.text.count('파이썬')}")
    except Exception as e:
        print(f"  {url.split('portal/')[-1]}: Error: {type(e).__name__}")

# POST JSON 시도
import json
for url in api_urls:
    try:
        r = session.post(url, json={"keyword": "파이썬", "page": 1, "size": 10},
                        headers={**HEADERS, 'Content-Type': 'application/json'}, timeout=5, verify=False)
        print(f"  POST {url.split('portal/')[-1]}: Status: {r.status_code}, CT: {r.headers.get('content-type','')[:30]}")
        if r.status_code == 200 and "파이썬" in r.text:
            print(f"    ★ POST MATCH! ★")
    except Exception as e:
        print(f"  POST Error: {type(e).__name__}")
