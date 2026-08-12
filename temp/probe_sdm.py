"""
서대문구 HTML 원문 확인
"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.sdm.go.kr/lib/"
r = session.get(url, headers=HEADERS, verify=False)
print(r.text)
