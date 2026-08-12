"""
김포시도서관 폼 액션 원본 텍스트 상세 분석
"""
from bs4 import BeautifulSoup

with open("gimpo_main.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
form = soup.select_one("#bookSearchForm, form[action*='bookSearch']")
if form:
    print("=== form html ===")
    print(form.prettify()[:1000])
else:
    print("No form found. Finding all forms:")
    for fm in soup.select("form"):
        print(f"  Form: action={fm.get('action')}")
