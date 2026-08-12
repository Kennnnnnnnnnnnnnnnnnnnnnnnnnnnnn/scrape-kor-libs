"""
의정부 HTML 내 '파이썬' 한글 단어 위치 정밀 분석
"""
import re

with open("uilib_search.html", "r", encoding="utf-8") as f:
    txt = f.read()

# '파이썬' 단어 매치 세기
matches = [m.start() for m in re.finditer("파이썬", txt)]
print(f"Total '파이썬' matches: {len(matches)}")

if matches:
    # 매치 주변 문맥을 디버그 파일로 저장
    with open("uilib_kwd_context.txt", "w", encoding="utf-8") as out:
        for idx, pos in enumerate(matches):
            out.write(f"\nMatch {idx} (Pos {pos}):\n")
            snippet = txt[max(0, pos-150):pos+200]
            out.write(snippet.strip().replace("\n", " ") + "\n")
    print("Saved context to uilib_kwd_context.txt")
else:
    print("No matches. Printing first 1000 characters of HTML:")
    print(txt[:1000])
