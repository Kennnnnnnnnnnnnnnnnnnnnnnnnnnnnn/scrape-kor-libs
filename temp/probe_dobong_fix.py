import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.unilib.dobong.kr/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&manage_code=MA,MB,MC,ME,MG,MJ,MF,MH,SA,MD,SB,SL,SM,SN,SO,SP,SK,SQ,SR,SS,ST,SU,SG,SH,SC&search_txt=%ED%8C%8C%EC%B9%9C%EC%BD%94"
r = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

items = soup.select("div.book_area, div.book_info_w")
print("Dobong items found:", len(items))

for idx, item in enumerate(items[:3], 1):
    call_tag = item.select_one("input[name='mb_callno_info']")
    c_val = call_tag.get("value") if call_tag else None
    
    dls = item.select("dl")
    dl_txt = [(dl.select_one("dt").text.strip() if dl.select_one("dt") else "", dl.select_one("dd").text.strip() if dl.select_one("dd") else "") for dl in dls]
    
    print(f"Item #{idx}: call_tag={c_val}, dl_txt={dl_txt}")
