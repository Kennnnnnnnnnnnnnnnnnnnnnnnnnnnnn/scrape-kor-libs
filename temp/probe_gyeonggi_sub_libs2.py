"""
서울특별시 미구현 구립도서관 10개 도메인 및 API 구조 일괄 탐색
"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

targets = [
    ("강북구립도서관", "https://www.gblib.or.kr"),
    ("관악구립도서관", "https://www.gwanaklib.seoul.kr"),
    ("광진구립도서관", "https://www.gjlib.or.kr"),
    ("구로구립도서관", "https://www.gurolib.or.kr"),
    ("금천구립도서관", "https://geumcheonlib.seoul.kr"),
    ("노원구립도서관", "https://www.nowonlib.kr"),
    ("도봉구립도서관", "https://www.unilib.dobong.kr"),
    ("동대문구립도서관", "https://www.l4d.or.kr"),
    ("서대문구립도서관", "https://www.sdmlib.or.kr"),
    ("성동구립도서관", "https://www.sdlib.or.kr")
]

for name, url in targets:
    try:
        r = session.get(url, headers=HEADERS, timeout=6, verify=False, allow_redirects=True)
        print(f"[{name}] {url} -> Status: {r.status_code}, Final: {r.url}, Len: {len(r.text)}")
    except Exception as e:
        print(f"[{name}] {url} -> Error: {e}")
