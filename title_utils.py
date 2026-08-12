"""
도서 제목 정제 유틸리티 (old/title.py 참조)
"""

def strip_title(val: str) -> str:
    if not val:
        return ""
    
    # 1. ']' 이전 부분 제거 (예: [도서] 파친코 -> 파친코)
    if ']' in val:
        val = val.split(']', maxsplit=1)[1]
        
    # 2. '합본:' 이전 부분 제거
    if "합본:" in val:
        val = val.split(':', maxsplit=1)[1]
        
    val = val.strip()
    
    # 3. 끝에 부가 설명 괄호가 붙어있을 경우 제거
    c = val.count(')')
    idx = val.rfind(')')
    if c > 0 and idx == len(val) - 1:
        idx_open = val.rfind('(')
        if idx_open != -1:
            val = val[:idx_open]
            
    # 4. 콜론 ':' 처리
    c = val.count(':')
    if c > 0:
        arr = val.split(':', maxsplit=2)
        if len(arr) == 1:
            val = arr[0]
        elif len(arr) == 2:
            val = arr[1]
        else:
            val = arr[1] + arr[2]
            
    val = val.strip()
    
    # 5. 너무 긴 검색어 제한 (70자 이하)
    if len(val) > 70:
        val = val[:69]
        
    return val
