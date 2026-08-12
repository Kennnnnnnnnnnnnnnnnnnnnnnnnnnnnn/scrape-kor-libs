"""
동작구 index_detail.do 텍스트 확인
"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.dongjak.go.kr/dj/intro/search/index_detail.do"
r = session.get(url, headers=HEADERS, verify=False)
print("index_detail content:")
print(r.text)
