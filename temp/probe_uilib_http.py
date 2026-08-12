"""
의정부시 도서관(uilib.go.kr) HTTP 프로토콜 직접 통신 다각도 진단 (allow_redirects=False)
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

CANDIDATES = [
    "http://www.uilib.go.kr/search/searchResultList.do",
    "http://www.uilib.go.kr/intro/searchResultList.do",
    "http://www.uilib.go.kr/intro/program/plusSearchResultList.do",
    "http://www.uilib.go.kr/intro/menu/10008/program/30001/plusSearchResultList.do",
    "http://www.uilib.go.kr/intro/menu/10041/program/30001/plusSearchResultList.do"
]

params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

for url in CANDIDATES:
    print(f"\nURL: {url}")
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=6, verify=False, allow_redirects=False)
        print(f"  Status: {r.status_code}, Length: {len(r.text)}")
        print(f"  Location Header: {r.headers.get('Location')}")
        if r.status_code == 200:
            print("  [SUCCESS!!!] 200 OK")
    except Exception as e:
        print(f"  Error: {e}")
