"""
biblioSearch.do AJAX 상세 분석
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("anseong_search_result.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find("function biblioSearch")
if idx != -1:
    print(html[idx:idx+1500])
