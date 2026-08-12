"""
송파구립도서관 결과 상세 구조 파싱
"""
from bs4 import BeautifulSoup
import re

with open("songpa_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1. 책 목록 영역 탐색
print("=== 1. 도서 목록 태그 탐색 ===")
# a 태그 중 href에 '/plusSearchResultDetail.do' 가 포함된 것이 있는지 검색
detail_links = soup.select("a[href*='plusSearchResultDetail']")
print(f"Detail links: {len(detail_links)}")
for lnk in detail_links[:5]:
    print(f"  Link href='{lnk.get('href')}' text='{lnk.text.strip()}'")

# 2. 첫 번째 책의 부모 li/div 데이터 전체 출력
if detail_links:
    first_p = detail_links[0].find_parent("li") or detail_links[0].find_parent("div")
    if first_p:
        print("\n=== 2. First Book Parent HTML ===")
        print(first_p.prettify()[:1500])
