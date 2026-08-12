"""
의정부 상세페이지 script[10] 내용 전체 덤프
"""
from bs4 import BeautifulSoup

with open("uijeongbu_detail.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
scripts = soup.select("script")

if len(scripts) > 10:
    print("=== Script[10] Context ===")
    print(scripts[10].text)
else:
    print("Script[10] not found.")
