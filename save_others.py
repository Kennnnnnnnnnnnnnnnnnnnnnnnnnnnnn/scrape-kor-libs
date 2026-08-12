import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

with open("others_out.txt", "w", encoding="utf-8") as f:
    # 1. 성동
    r_sd = requests.get("https://www.sdlib.or.kr/SD/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&use_facet=N&main_type=Y&search_txt=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)
    soup_sd = BeautifulSoup(r_sd.text, "html.parser")
    item_sd = soup_sd.select_one("div.book_info_w")
    f.write("=== Seongdong ===\n")
    if item_sd:
        f.write(item_sd.text.strip() + "\n\n")

    # 2. 서대문
    r_sdm = requests.get("https://lib.sdm.or.kr/sdmlib/menu/10003/program/30001/searchResultList.do?searchType=SIMPLE&searchCategory=ALL&searchKey=ALL&searchLibrary=ALL&searchKeyword=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)
    soup_sdm = BeautifulSoup(r_sdm.text, "html.parser")
    item_sdm = soup_sdm.select_one("div.book_dataInner")
    f.write("=== Seodaemun ===\n")
    if item_sdm:
        f.write(item_sdm.text.strip() + "\n\n")

    # 3. 종로
    r_jn = requests.get("https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php?library=ALL&search_type=normal&search_value=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)
    soup_jn = BeautifulSoup(r_jn.text, "html.parser")
    item_jn = soup_jn.select_one("li.book_top_info, div.book_name, ul.book_list > li")
    f.write("=== Jongno ===\n")
    if item_jn:
        f.write(item_jn.text.strip() + "\n\n")

    # 4. 중구
    r_jg = requests.get("https://www.junggulib.or.kr/SJGL/program/searchResultList.do?searchType=SIMPLE&searchCategory=ALL&searchKey=ALL&searchLibrary=ALL&searchKeyword=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)
    soup_jg = BeautifulSoup(r_jg.text, "html.parser")
    item_jg = soup_jg.select_one("div.book_dataInner")
    f.write("=== Junggu ===\n")
    if item_jg:
        f.write(item_jg.text.strip() + "\n\n")

print("Saved to others_out.txt")
