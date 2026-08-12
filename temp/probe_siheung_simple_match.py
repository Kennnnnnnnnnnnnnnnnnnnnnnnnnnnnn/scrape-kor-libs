"""
시흥시 main.js 내 단순 텍스트 매칭 개수 및 일부 블록 출력
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

print("File Length:", len(txt))
print("HOME_PAGE_ID count:", txt.count("HOME_PAGE_ID"))
print("API_URL count:", txt.count("API_URL"))
print("pyxis-api count:", txt.count("pyxis-api"))

# 첫 500글자
print("\n=== START SNIPPET ===")
print(txt[:500])
