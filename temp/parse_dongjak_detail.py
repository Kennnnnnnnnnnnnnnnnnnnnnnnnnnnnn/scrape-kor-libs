"""
동작구립도서관 결과 상세 구조 파싱
"""
from bs4 import BeautifulSoup
import re

with open("dongjak_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 총 건수
print("=== 1. 총 건수 태그 찾기 ===")
text_nodes = soup.find_all(text=True)
for node in text_nodes:
    val = node.strip()
    if val and any(w in val for w in ["결과", "전체", "총"]) and re.search(r'\d+', val) and len(val) < 50:
        print(f"Match: <{node.parent.name}> class={node.parent.get('class')} text='{val}'")

# 2. 책 목록 분석
print("\n=== 2. 책 목록 테이블/리스트 구조 ===")
# a 태그 중 href에 '/detail/' 이나 '/book/' 이 포함된 경로가 있는지 확인
detail_links = soup.select("a[href*='detail']")
print(f"Detail links count: {len(detail_links)}")
for lnk in detail_links[:10]:
    print(f"  Link: href='{lnk.get('href')}', text='{lnk.text.strip()}'")
