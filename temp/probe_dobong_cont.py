import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.unilib.dobong.kr/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&manage_code=MA,MB,MC,ME,MG,MJ,MF,MH,SA,MD,SB,SL,SM,SN,SO,SP,SK,SQ,SR,SS,ST,SU,SG,SH,SC&search_txt=%ED%8C%8C%EC%B9%9C%EC%BD%94"
r = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

item = soup.select_one("div.book_info_w")
if item:
    cont_div = item.select_one("div.cont")
    print("cont_div html:")
    print(cont_div.prettify() if cont_div else "No cont_div")
