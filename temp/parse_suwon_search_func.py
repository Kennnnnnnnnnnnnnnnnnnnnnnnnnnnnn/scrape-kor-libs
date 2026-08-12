"""
수원 search.js 내 search 함수 정의 본문 추출 및 분석
"""
with open("suwon_search.js", "r", encoding="utf-8") as f:
    txt = f.read()

# 'function search(' 를 찾아서 그 이후의 내용 파악
idx = txt.find("function search(")
if idx != -1:
    print("=== Search function found ===")
    # 대괄호 '{' 와 '}' 쌍의 매칭을 찾아 함수 본문만 슬라이싱
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
    print("search function not found")
