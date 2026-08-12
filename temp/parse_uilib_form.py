"""
의정부시 도서관 mainSearchForm 상세 덤프 및 분석
"""
from bs4 import BeautifulSoup

with open("uilib_real_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# mainSearchForm 폼 검색
form = soup.select_one("form#mainSearchForm, form[name*='mainSearch'], form[action*='Search']")
if form:
    print("=== mainSearchForm found ===")
    print(f"Action: {form.get('action')}")
    print(f"Method: {form.get('method')}")
    for inp in form.select("input, select, textarea"):
        print(f"  <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
else:
    print("No mainSearchForm found. Listing all forms:")
    for i, fm in enumerate(soup.select("form")):
        print(f"  Form[{i}] id={fm.get('id')} action={fm.get('action')} method={fm.get('method')}")
