"""
AnseongScraper 파싱 과정 디버그 스크립트
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

print("dls count:", len(dls))

for dl in dls:
    title_tag = dl.select_one("dd > a")
    book_title = title_tag.text.strip() if title_tag else "None"
    
    biblio_id = None
    for a_btn in dl.select("a, button"):
        onc = a_btn.get("onclick", "")
        m = re.search(r"(?:goView|biblioSearch)\(\s*(\d+(?:\.\d+)?)", onc)
        if m:
            biblio_id = str(int(float(m.group(1))))
            break
            
    print(f"Title: {book_title[:30]} | biblio_id: {biblio_id}")
    
    if biblio_id:
        api_url = "https://www.anseong.go.kr/library/search/biblioSearch.do"
        api_resp = session.post(api_url, data={"biblioId": biblio_id}, headers=HEADERS, timeout=6, verify=False)
        print(f"  API status: {api_resp.status_code}, len: {len(api_resp.text)}")
        print(f"  Text: {api_resp.text[:150]}")
