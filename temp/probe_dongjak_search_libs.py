"""
동작구 AJAX 및 search.do 엔드포인트 탐색
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111'
}

session.get("https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111", headers=HEADERS, verify=False)

urls = [
    "https://lib.dongjak.go.kr/dj/intro/search/search.do",
    "https://lib.dongjak.go.kr/dj/intro/search/searchList.do",
    "https://lib.dongjak.go.kr/dj/intro/search/resultList.do",
    "https://lib.dongjak.go.kr/dj/intro/search/index_detail.do"
]

params = {
    "menu_idx": "111",
    "search_text": "파이썬",
    "search_type": "ALL"
}

for url in urls:
    try:
        r_get = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        r_post = session.post(url, data=params, headers=HEADERS, timeout=8, verify=False)
        print(f"URL: {url} -> GET: {r_get.status_code} (len: {len(r_get.text)}), POST: {r_post.status_code} (len: {len(r_post.text)})")
        if r_get.text.count("파이썬") > 1 or r_post.text.count("파이썬") > 1:
            print("  ★ DONGJAK AJAX SEARCH MATCH ★")
    except Exception as e:
        print(f"Error: {e}")
