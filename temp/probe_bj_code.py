import requests, urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 1. intro searchManageCode 미지정 (또는 ALL)
r1 = requests.get("https://www.hscitylib.or.kr/intro/menu/10003/program/30001/searchResultList.do?searchType=SIMPLE&searchKeyword=the+chronicles+of+Narnia&searchManageCode=ALL&searchDisplay=100", headers=headers, verify=False)
soup1 = BeautifulSoup(r1.text, "html5lib")
items1 = soup1.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")

# 2. bjlib (병점도서관 전용 경로)
r2 = requests.get("https://www.hscitylib.or.kr/bjlib/menu/10553/program/30001/searchResultList.do?searchType=SIMPLE&searchKeyword=the+chronicles+of+Narnia&searchManageCode=ALL&searchDisplay=100", headers=headers, verify=False)
soup2 = BeautifulSoup(r2.text, "html5lib")
items2 = soup2.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")

# 3. bjlib 경로에서 searchManageCode=MA_BJ (병점도서관 관코드)
r3 = requests.get("https://www.hscitylib.or.kr/bjlib/menu/10553/program/30001/searchResultList.do?searchType=SIMPLE&searchKeyword=the+chronicles+of+Narnia&searchManageCode=MA_BJ&searchDisplay=100", headers=headers, verify=False)
soup3 = BeautifulSoup(r3.text, "html5lib")
items3 = soup3.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")

print("1. intro ALL total items:", len(items1))
print("2. bjlib ALL total items:", len(items2))
print("3. bjlib MA_BJ (병점관 전용) total items:", len(items3))
