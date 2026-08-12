"""
안성시도서관 결과 HTML 내 viewForm 정의부 정밀 덤프
"""
from bs4 import BeautifulSoup

with open("anseong_real_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
vform = soup.select_one("form#viewForm, form[id*='view']")

if vform:
    print("=== viewForm found ===")
    print(vform.prettify())
else:
    print("No viewForm found. Listing all forms in result:")
    for i, fm in enumerate(soup.select("form")):
        print(f"  Form[{i}] id={fm.get('id')} action={fm.get('action')} method={fm.get('method')}")
        for inp in fm.select("input"):
            print(f"    input name={inp.get('name')} value={inp.get('value')}")
