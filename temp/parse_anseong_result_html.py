"""
안성시 검색 결과 html 상세 파싱 분석
"""
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("anseong_search_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 키워드 위치 확인
idx = html.find("파이썬")
print(f"=== '파이썬' 주변 300자 ({idx}) ===")
if idx != -1:
    print(html[max(0, idx-100):min(len(html), idx+200)].strip())

# 모든 폼 및 테이블/리스트 요소 탐색
print("\n=== All forms ===")
for i, form in enumerate(soup.select("form")):
    print(f"  Form[{i}] action='{form.get('action')}' id='{form.get('id')}'")

print("\n=== Elements with class containing 'list', 'item', 'book', 'result' ===")
for el in soup.select("[class*='list'], [class*='item'], [class*='book'], [class*='result']"):
    cls = el.get("class", [])
    tag = el.name
    # 너무 일반적인 태그 제외
    if tag in ["div", "ul", "ol", "table", "tbody", "section"]:
        txt = el.text.strip()[:60].replace("\n", " ")
        if len(txt) > 5:
            print(f"  <{tag}> class={cls}: '{txt}'")
            if len(el.select("li, tr, div")) > 0:
                print(f"    Direct children: {len(el.find_all(recursive=False))}")
