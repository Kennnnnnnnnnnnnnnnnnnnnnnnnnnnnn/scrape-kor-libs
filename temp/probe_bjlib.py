import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 1. intro URL
url_intro = "https://www.hscitylib.or.kr/intro/menu/10003/program/30001/searchResultList.do"
params_intro = {
    "searchType": "SIMPLE",
    "searchKeyword": "the chronicles of Narnia",
    "searchManageCode": "ALL",
    "searchDisplay": "100"
}

r1 = requests.get(url_intro, params=params_intro, headers=headers, verify=False, timeout=15)
s1 = BeautifulSoup(r1.text, "html5lib")
cnt1 = s1.select_one("#totalCnt")
print(f"intro URL TotalCnt: {cnt1.text.strip() if cnt1 else 'N/A'}")

# 2. bjlib URL
url_bj = "https://www.hscitylib.or.kr/bjlib/menu/10553/program/30001/searchResultList.do"
params_bj = {
    "searchType": "SIMPLE",
    "searchKeyword": "the chronicles of Narnia",
    "searchManageCode": "ALL",
    "searchDisplay": "100"
}

r2 = requests.get(url_bj, params=params_bj, headers=headers, verify=False, timeout=15)
s2 = BeautifulSoup(r2.text, "html5lib")
cnt2 = s2.select_one("#totalCnt")
print(f"bjlib URL TotalCnt: {cnt2.text.strip() if cnt2 else 'N/A'}")

def get_libs(soup):
    libs = defaultdict(int)
    for item in soup.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li"):
        loc_tag = item.select_one("div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(4) > span")
        if loc_tag:
            m = re.search(r'\[(.+?)\]', loc_tag.text.strip())
            if m:
                libs[m.group(1)] += 1
    return libs

from collections import defaultdict
print("\nintro URL libraries:", dict(get_libs(s1)))
print("\nbjlib URL libraries:", dict(get_libs(s2)))
