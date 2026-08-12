import requests, urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 현재 스크래퍼가 사용하는 URL
url1 = "https://www.hscitylib.or.kr/intro/menu/10003/program/30001/searchResultList.do"
params1 = {"searchType":"SIMPLE","searchKeyword":"파친코","searchArticle":"SCORE","searchOrder":"ASC"}

# 사용자가 보낸 URL (bjlib)
url2 = "https://www.hscitylib.or.kr/bjlib/menu/10553/program/30001/searchResultList.do"
params2 = {"searchType":"SIMPLE","searchKeyword":"파친코","searchManageCode":"ALL","searchDisplay":"20"}

r1 = requests.get(url1, params=params1, headers=headers, verify=False, timeout=15)
s1 = BeautifulSoup(r1.text, "html5lib")
cnt1 = s1.select_one("#totalCnt")
cnt1_text = cnt1.text.strip() if cnt1 else "N/A"
print(f"[intro URL] totalCnt={cnt1_text}")
items1 = s1.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")
print(f"[intro URL] items on page: {len(items1)}")

r2 = requests.get(url2, params=params2, headers=headers, verify=False, timeout=15)
s2 = BeautifulSoup(r2.text, "html5lib")
cnt2 = s2.select_one("#totalCnt")
cnt2_text = cnt2.text.strip() if cnt2 else "N/A"
print(f"[bjlib URL] totalCnt={cnt2_text}")
items2 = s2.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")
print(f"[bjlib URL] items on page: {len(items2)}")

# searchManageCode=ALL 추가해서 intro URL 재시도
params3 = dict(params1)
params3["searchManageCode"] = "ALL"
params3["searchDisplay"] = "100"
r3 = requests.get(url1, params=params3, headers=headers, verify=False, timeout=15)
s3 = BeautifulSoup(r3.text, "html5lib")
cnt3 = s3.select_one("#totalCnt")
cnt3_text = cnt3.text.strip() if cnt3 else "N/A"
print(f"[intro+ALL+100] totalCnt={cnt3_text}")
items3 = s3.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")
print(f"[intro+ALL+100] items on page: {len(items3)}")

# 각 도서관 이름 출력
import re
libs = set()
for item in items3:
    loc_tag = item.select_one("div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(4) > span")
    if loc_tag:
        loc_text = loc_tag.text.strip()
        match = re.search(r'\[(.+?)\]', loc_text)
        if match:
            libs.add(match.group(1))
print(f"\n[intro+ALL+100] 도서관 목록: {sorted(libs)}")
