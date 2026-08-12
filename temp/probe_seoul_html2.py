import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. 도봉
r_db = requests.get("https://www.unilib.dobong.kr/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&manage_code=MA,MB,MC,ME,MG,MJ,MF,MH,SA,MD,SB,SL,SM,SN,SO,SP,SK,SQ,SR,SS,ST,SU,SG,SH,SC&search_txt=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)
soup_db = BeautifulSoup(r_db.text, "html.parser")
item_db = soup_db.select_one("div.book_area, div.book_info_w")
print("=== Dobong Item ===")
if item_db:
    print(item_db.prettify()[:1000])

# 2. 성동
r_sd = requests.get("https://www.sdlib.or.kr/SD/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&use_facet=N&main_type=Y&search_txt=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)
soup_sd = BeautifulSoup(r_sd.text, "html.parser")
item_sd = soup_sd.select_one("div.book_info_w")
print("\n=== Seongdong Item ===")
if item_sd:
    print(item_sd.prettify()[:1000])
