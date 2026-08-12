import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 사용자가 준 URL 그대로 요청
url = "https://www.hscitylib.or.kr/bjlib/menu/10553/program/30001/searchResultList.do"
params = {
    "searchType": "SIMPLE",
    "viewType": "LIST",
    "searchKeyword": "the chronicles of Narnia",
    "searchPubFormCode": "ALL",
    "currentPageNo": "1",
    "searchDisplay": "100", # 100건으로 요청
    "searchArticle": "SCORE",
    "searchOrder": "ASC",
    "reSearchYn": "N",
    "searchManageCode": "ALL"
}

resp = requests.get(url, params=params, headers=headers, verify=False, timeout=15)
soup = BeautifulSoup(resp.text, "html5lib")

items = soup.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")
print(f"Total items in 1st page (searchDisplay=100): {len(items)}")

bj_items = []
all_parsed = []
for idx, item in enumerate(items, 1):
    loc_tag = item.select_one("div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(4) > span")
    loc_text = loc_tag.text.strip() if loc_tag else ""
    
    tit_tag = item.select_one("div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > p > a")
    tit_text = tit_tag.get("title", tit_tag.text.strip()) if tit_tag else ""

    all_parsed.append((idx, tit_text, loc_text))
    if "병점" in loc_text:
        bj_items.append((idx, tit_text, loc_text))

print(f"\n병점도서관 검색 결과 개수: {len(bj_items)}")
for idx, t, loc in bj_items:
    print(f" #{idx} | Title: {t} | Loc: {loc}")

print("\n전체 수집된 location 목록 (상위 20개):")
for idx, t, loc in all_parsed[:20]:
    print(f" #{idx} | Loc: {loc} | Title: {t}")
