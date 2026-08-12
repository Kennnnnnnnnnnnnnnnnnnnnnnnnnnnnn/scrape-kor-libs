"""
양주시도서관 전체 지점 코드 리스트 수집
"""
from bs4 import BeautifulSoup

with open("yangju_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# select 내 searchLibrary 및 options 탐색
select_tags = soup.select("select[name*='Library'], select[id*='Library'], select[name*='Lib'], select[id*='Lib']")
print(f"Library Select tags: {len(select_tags)}")

for idx, sel in enumerate(select_tags):
    print(f"  [{idx}] name={sel.get('name')} id={sel.get('id')}")
    for opt in sel.select("option"):
        print(f"    Option value='{opt.get('value')}' txt='{opt.text.strip()}'")
        
# 폼 내부에 option 이 있는지 일반 탐색
options = soup.select("option")
print(f"All options count: {len(options)}")
for opt in options[:40]:
    val = opt.get('value', '')
    txt = opt.text.strip().replace('\n', ' ')
    if any(w in txt for w in ["도서관", "중앙", "꿈나무", "희망", "덕계"]):
        print(f"  Option: value='{val}' txt='{txt}'")
