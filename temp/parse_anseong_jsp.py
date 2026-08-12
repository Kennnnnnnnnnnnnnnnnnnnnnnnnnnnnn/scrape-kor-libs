"""
안성시 Search.jsp 결과 파싱 구조 분석
"""
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("anseong_search_jsp.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 키워드 위치 확인
idx = html.find("파이썬")
while idx != -1:
    print(f"\n=== '파이썬' 주변 200자 ({idx}) ===")
    print(html[max(0, idx-100):min(len(html), idx+150)].strip())
    idx = html.find("파이썬", idx + 1)
