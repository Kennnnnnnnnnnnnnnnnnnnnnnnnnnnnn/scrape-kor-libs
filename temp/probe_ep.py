"""
은평구립도서관 bookList[0] 필드 상세 확인
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.eplib.or.kr/unified/search.asp'
}

url = "https://www.eplib.or.kr/api/search"
payload = {
    "searchKeyword": "파이썬",
    "page": 1,
    "display": 5,
    "selectedLibraries": ["ALL"]
}

r = session.post(url, json=payload, headers=HEADERS, timeout=10, verify=False)
data = r.json()
book0 = data['contents']['bookList'][0]
print(json.dumps(book0, ensure_ascii=False, indent=2))
