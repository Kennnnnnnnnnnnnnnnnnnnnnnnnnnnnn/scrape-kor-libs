"""
동작구립 common.js 내 doAjaxLoad 및 doAjaxPost 함수 본문 추출
"""
with open("common.js", "r", encoding="utf-8") as f:
    txt = f.read()

# doAjaxLoad 또는 doAjaxPost 함수 정의 찾기
for func_name in ["doAjaxLoad", "doAjaxPost"]:
    idx = txt.find(f"function {func_name}")
    if idx != -1:
        print(f"\n=== {func_name} definition ===")
        print(txt[idx:idx+800].replace("\n", " "))
