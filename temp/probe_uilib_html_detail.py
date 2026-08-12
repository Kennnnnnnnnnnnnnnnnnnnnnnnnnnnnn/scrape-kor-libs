"""
의정부 HTML 저장 파일 상세 진단 (인코딩 우회 및 빈 화면 여부 확인)
"""
from bs4 import BeautifulSoup

# 파일 읽기
with open("uilib_search.html", "r", encoding="utf-8") as f:
    txt = f.read()

print("HTML Length:", len(txt))
print("HTML Title:", BeautifulSoup(txt, "html.parser").title.text if BeautifulSoup(txt, "html.parser").title else "No Title")

# input 태그 전부 덤프
soup = BeautifulSoup(txt, "html.parser")
inputs = soup.select("input")
print(f"Inputs found: {len(inputs)}")
for inp in inputs:
    print(f"  <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
