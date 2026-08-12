"""
서울 미구현 도서관 일괄 도메인/API 탐색
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

targets = [
    # (이름, URL 후보들)
    ("강동구립도서관", [
        "https://www.gdlibrary.or.kr",
        "https://lib.gangdong.go.kr",
        "https://www.gangdonglib.or.kr",
    ]),
    ("강북구립도서관", [
        "https://www.gblib.or.kr",
        "https://lib.gangbuk.go.kr",
        "https://www.gangbuklib.or.kr",
    ]),
    ("관악구립도서관", [
        "https://www.gwanaklib.or.kr",
        "https://lib.gwanak.go.kr",
        "https://www.galib.or.kr",
    ]),
    ("광진구립도서관", [
        "https://www.gwangjinlib.or.kr",
        "https://lib.gwangjin.go.kr",
        "https://www.gjlib.or.kr",
    ]),
    ("구로구립도서관", [
        "https://www.gurolib.or.kr",
        "https://lib.guro.go.kr",
        "https://www.gurolib.seoul.kr",
    ]),
    ("금천구립도서관", [
        "https://lib.geumcheon.go.kr",
        "https://www.gclib.or.kr",
        "https://www.geumcheonlib.or.kr",
    ]),
    ("마포구립도서관", [
        "https://www.mapolib.or.kr",
        "https://lib.mapo.go.kr",
        "https://www.mapolib.seoul.kr",
    ]),
    ("서대문구립도서관", [
        "https://www.sdm.go.kr/lib/",
        "https://lib.sdm.go.kr",
    ]),
    ("성동구립도서관", [
        "https://www.sdlib.or.kr",
        "https://lib.sd.go.kr",
        "https://lib.seongdong.go.kr",
        "https://www.seongdonglib.or.kr",
    ]),
    ("양천구립도서관", [
        "https://lib.yangcheon.go.kr",
        "https://www.yangcheonlib.or.kr",
        "https://www.yclib.or.kr",
    ]),
    ("용산구립도서관", [
        "https://yslibrary.or.kr",
        "https://lib.yongsan.go.kr",
        "https://www.yslib.or.kr",
    ]),
    ("은평구립도서관", [
        "https://www.eplib.or.kr",
    ]),
    ("중구립도서관", [
        "https://www.junggulib.or.kr",
        "https://lib.junggu.go.kr",
        "https://www.jglib.or.kr",
        "https://lib.jung.go.kr",
    ]),
]

for name, urls in targets:
    print(f"\n=== {name} ===")
    for url in urls:
        try:
            r = session.get(url, headers=HEADERS, timeout=5, verify=False, allow_redirects=True)
            print(f"  ✅ {url} -> Status: {r.status_code}, Final: {r.url[:60]}, Len: {len(r.text)}")
        except Exception as e:
            print(f"  ❌ {url} -> Error: {type(e).__name__}")
