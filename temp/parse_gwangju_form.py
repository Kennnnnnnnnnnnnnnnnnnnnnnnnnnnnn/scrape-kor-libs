"""
광주시도서관 통합검색 폼 및 스크립트 이벤트 정밀 분석
"""
from bs4 import BeautifulSoup

with open("gwangju_real_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# libSearch2 및 모든 form 탐색
print("=== Forms in Gwangju Real Main ===")
for i, form in enumerate(soup.select("form")):
    print(f"Form[{i}] id={form.get('id')} action={form.get('action')} onsubmit={form.get('onsubmit')}")
    for inp in form.select("input, select, button"):
        print(f"  <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")

# 스크립트 분석
for sc_idx, sc in enumerate(soup.select("script")):
    txt = sc.text
    if "libSearch" in txt or "searchKeyword" in txt or "resultList" in txt:
        print(f"\n=== Script[{sc_idx}] ===")
        for line in txt.split("\n"):
            if "action" in line or "submit" in line or "location" in line or "libSearch" in line:
                print("  ", line.strip()[:150])
