"""
AnseongScraper branchId 추출 테스트
"""
import requests
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.anseong.go.kr/library/search/search.do?mId=0101010100"
payload = {"searchKeyType": "K", "searchTxt": "파이썬"}

r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
soup = BeautifulSoup(r.text, "html.parser")
dls = soup.select("div.anseong-search-list-table dl")

for dl in dls:
    title_tag = dl.select_one("dd > a")
    book_title = title_tag.text.strip() if title_tag else "None"
    
    biblio_id = None
    branch_id = None
    for a_btn in dl.select("a, button"):
        onc = a_btn.get("onclick", "")
        m = re.search(r"biblioSearch\(\s*(\d+(?:\.\d+)?)\s*,\s*['\"]?[^'\"]*['\"]?\s*,\s*(\d+)", onc)
        if m:
            biblio_id = str(int(float(m.group(1))))
            branch_id = m.group(2)
            break
            
    print(f"Title: {book_title[:25]} | biblio_id: {biblio_id} | branch_id: {branch_id}")
    
    if biblio_id:
        api_url = "https://www.anseong.go.kr/library/search/biblioSearch.do"
        post_data = {"biblioId": biblio_id}
        if branch_id:
            post_data["branchId"] = branch_id
        api_resp = session.post(api_url, data=post_data, headers=HEADERS, timeout=6, verify=False)
        print(f"  API status: {api_resp.status_code}, len: {len(api_resp.text)}")
        if api_resp.status_code == 200:
            res = api_resp.json()
            if res.get("success"):
                items = res.get("data", {}).get("list", [])
                for it in items:
                    print(f"    Item: {it.get('branch', {}).get('name')} | {it.get('location', {}).get('name')} | {it.get('callNo')}")
