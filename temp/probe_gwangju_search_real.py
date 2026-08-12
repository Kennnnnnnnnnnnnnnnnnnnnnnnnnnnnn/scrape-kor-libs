"""
광주시 GET 50 bytes 텍스트 내용 확인
"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
r = session.get(url, params={"searchKeyword": "파이썬", "searchType": "SIMPLE"}, headers=HEADERS, verify=False)
print("50 bytes content:")
print(repr(r.text))
