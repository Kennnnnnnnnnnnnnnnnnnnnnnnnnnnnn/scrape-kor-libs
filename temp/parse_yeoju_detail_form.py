"""
여주시도서관 fnSearchResultDetail 함수 인자 추출 및 goView/detail 폼 형태 분석
"""
from bs4 import BeautifulSoup
import re

with open("yeoju_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1. fnSearchResultDetail 호출이 들어간 onclick 속성들 덤프
a_onclicks = [a.get("onclick") for a in soup.select("a") if a.get("onclick") and "fnSearchResultDetail" in a.get("onclick")]
print(f"fnSearchResultDetail onclicks: {len(a_onclicks)}")
for idx, clk in enumerate(a_onclicks[:10]):
    print(f"  [{idx}] {clk}")

# 2. 결과 화면에 정의된 bookForm 이나 detailForm 덤프
bform = soup.select_one("form#bookForm")
if bform:
    print("\n=== bookForm found ===")
    print(bform.prettify())
else:
    print("\nNo bookForm found in result")
