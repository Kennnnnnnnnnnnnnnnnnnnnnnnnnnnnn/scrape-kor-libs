"""
수원 search.js 내 getSearchParam 함수 정의 본문 추출 및 분석
"""
with open("suwon_search.js", "r", encoding="utf-8") as f:
    txt = f.read()

idx = txt.find("function getSearchParam(")
if idx != -1:
    print("=== getSearchParam function found ===")
    bracket_count = 0
    start_pos = txt.find("{", idx)
    end_pos = start_pos
    
    if start_pos != -1:
        for i in range(start_pos, len(txt)):
            if txt[i] == '{':
                bracket_count += 1
            elif txt[i] == '}':
                bracket_count -= 1
                if bracket_count == 0:
                    end_pos = i
                    break
        print(txt[idx:end_pos+1])
else:
    print("getSearchParam function not found")
