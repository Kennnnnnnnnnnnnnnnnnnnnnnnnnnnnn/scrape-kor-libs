"""
동작구립도서관 Form 태그 내부 상세 input 분석
"""
from bs4 import BeautifulSoup

with open("dongjak_search_with_libs.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

form = soup.select_one("form")
if form:
    print(f"Form action={form.get('action')} method={form.get('method')}")
    # 모든 input, select, textarea 덤프
    for inp in form.select("input, select, textarea"):
        print(f"  <{inp.name}> name='{inp.get('name')}', value='{inp.get('value')}', id='{inp.get('id')}', type='{inp.get('type')}'")
else:
    print("Form not found in HTML")
