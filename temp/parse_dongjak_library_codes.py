"""
동작구립도서관 도서관 코드(libraryCodes) 옵션값 추출
"""
from bs4 import BeautifulSoup

with open("dongjak_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# select[name=libraryCodes] 또는 select[name=search_library] 의 option 값들을 덤프
select_tags = soup.select("select[name*=library], select[name*=Library]")
print(f"Library select tags count: {len(select_tags)}")
for sel in select_tags:
    print(f"Select: name={sel.get('name')}, id={sel.get('id')}")
    options = sel.select("option")
    for opt in options[:10]:
        print(f"  Option: value='{opt.get('value')}', text='{opt.text.strip()}'")
