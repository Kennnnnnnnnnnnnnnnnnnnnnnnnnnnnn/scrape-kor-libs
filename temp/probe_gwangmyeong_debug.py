"""
광명시도서관 진짜 도서 카드 셀렉터(:has) 검증 디버깅 3
"""
import requests
from bs4 import BeautifulSoup
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://gmlib.gm.go.kr/dls_le/index.php"

params = {
    "mod": "wdDataSearch",
    "act": "searchIList",
    "item": "total",
    "word": "파이썬"
}

try:
    r = requests.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # input.listCheck 가 들어있는 div.list 만 셀렉트
    items = []
    for div in soup.select("div.list"):
        if div.select_one("input.listCheck") or div.select_one(".listCheck"):
            items.append(div)
            
    print(f"Total REAL list items: {len(items)}")
    
    for idx, item in enumerate(items[:4]):
        # 제목: input.listCheck의 title 속성에 이미 한글 책 제목이 들어있음!
        # 예: title="파이썬 프로그램 책"
        chk = item.select_one("input.listCheck")
        chk_title = chk.get("title", "").replace(" 선택", "").replace("선택", "").strip() if chk else ""
        
        # 상세 링크 찾기
        detail_link = None
        for a_tag in item.select("a"):
            href = a_tag.get("href", "")
            if "searchResultDetail" in href:
                detail_link = a_tag
                break
                
        if not detail_link:
            print(f"  [{idx}] '{chk_title}' -> No detail link found.")
            continue
            
        href = detail_link.get("href", "")
        m_jong = re.search(r"jongKey=([^&]+)", href)
        m_book = re.search(r"bookKey=([^&]+)", href)
        if not m_jong or not m_book:
            print(f"  [{idx}] '{chk_title}' -> Failed to parse keys from: {href}")
            continue
            
        jong_key = m_jong.group(1).strip()
        book_key = m_book.group(1).strip()
        
        # 상세 소장처 조회
        d_params = {
            "mod": "wdDataSearch",
            "act": "searchResultDetail",
            "dbType": "dan",
            "jongKey": jong_key,
            "bookKey": book_key
        }
        
        d_resp = requests.get(url, params=d_params, headers=HEADERS, timeout=8, verify=False)
        dsoup = BeautifulSoup(d_resp.text, "html.parser")
        rows = dsoup.select("table tbody tr")
        
        print(f"\n--- Book[{idx}] '{chk_title}' -> Rows: {len(rows)} ---")
        for r_idx, row in enumerate(rows):
            tds = row.select("td")
            if len(tds) >= 4:
                raw_call = tds[2].text.replace("청구기호", "").replace("인쇄", "").strip()
                clean_call = raw_call.replace("\n", "").replace("\r", "").replace("\t", "").strip()
                
                # 가공 로직 적용
                lib_name = tds[1].text.strip()
                call_no = ""
                shelf_loc = ""
                
                if clean_call.startswith("[") and "]" in clean_call:
                    idx_end = clean_call.find("]")
                    lib_loc = clean_call[1:idx_end].strip()
                    book_loc = clean_call[idx_end+1:].strip()
                    
                    parts = book_loc.split()
                    if len(parts) >= 2:
                        if len(parts) >= 3 and len(parts[-2]) == 1:
                            call_no = parts[-2] + " " + parts[-1]
                            shelf_loc = " ".join(parts[:-2])
                        else:
                            call_no = parts[-1]
                            shelf_loc = " ".join(parts[:-1])
                    else:
                        call_no = book_loc
                        shelf_loc = ""
                else:
                    call_no = clean_call
                    shelf_loc = ""
                    
                print(f"  Row[{r_idx}] -> raw='{raw_call}'")
                print(f"            -> clean='{clean_call}'")
                print(f"            -> lib='{lib_name}', call='{call_no}', loc='{shelf_loc}'")
except Exception as e:
    print("Error:", e)
