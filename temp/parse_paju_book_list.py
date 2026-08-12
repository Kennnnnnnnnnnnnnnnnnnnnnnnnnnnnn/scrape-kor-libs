"""
파주시 도서관 결과 HTML 84000~95000 바이트 영역 정밀 덤프
"""
with open("paju_result.html", "r", encoding="utf-8") as f:
    html = f.read()

snippet = html[83700:88000]
print(snippet.replace("\n", " ").strip())
