"""
금천구 AJAX 응답 상세 필드 확인
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
session.get("https://geumcheonlib.seoul.kr/geumcheonlib/uce/search/totalList.do?selfId=1097",
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
    verify=False)

r = session.post("https://geumcheonlib.seoul.kr/book/bookSearchList",
    data={"searchKeyword": "파이썬", "page": 1, "article": "TITLE", "display": 10, "manageCode": "ALL"},
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://geumcheonlib.seoul.kr/geumcheonlib/uce/search/totalList.do?selfId=1097',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }, verify=False)

data = r.json()
print("Keys:", list(data.keys()))
print("searchLibList:", json.dumps(data.get("searchLibList", [])[:3], ensure_ascii=False, indent=2))
print("\nbookList[0] keys:", list(data.get("bookList", [{}])[0].keys()) if data.get("bookList") else "EMPTY")
if data.get("bookList"):
    print("bookList[0]:", json.dumps(data["bookList"][0], ensure_ascii=False, indent=2)[:500])
