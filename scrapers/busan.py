"""
부산도서관 스크래퍼
https://library.busan.go.kr
"""
import re
import requests
from bs4 import BeautifulSoup

from .base import LibraryScraper, BookInfo
from .registry import register_scraper


DISTRICT_LIB_CODES = {
    "해운대구": ["BD", "BR", "AT", "AC", "AZ", "AL"],
    "금정구": ["AP", "BY"],
    "사하구": ["AE", "BC", "CE"],
    "부산진구": ["AG", "AD", "BA", "BL", "CD", "CH"],
    "동래구": ["AN", "BK", "BP"],
    "남구": ["AQ", "JT", "CG"],
    "북구": ["AB", "BE", "AU", "BN", "CJ"],
    "기장군": ["AX", "BJ", "KP", "BZ", "CA", "CL", "CM", "BG"],
    "강서구": ["AR", "BM", "CI"],
    "연제구": ["AJ", "BH", "CC", "KN"],
    "수영구": ["AV", "AY", "AO"],
    "영도구": ["AM", "BB"],
    "중구": ["AK"],
    "서구": ["AA", "CK"],
    "동구": ["AS", "BT", "AH"],
    "사상구": ["BS", "AW", "CF"]
}


class BusanScraper(LibraryScraper):
    """부산도서관 및 부산 광역시 자치구/군 공공도서관 통합 스크래퍼"""

    def __init__(self, region_name="부산도서관"):
        super().__init__(
            region_name=region_name,
            base_url="https://library.busan.go.kr/portal/intro/search/index.do"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        search_kw = f"{title} {author}".strip() if author else title
        
        params = [
            ("menu_idx", "14"),
            ("title", search_kw),
            ("search_text", search_kw),
            ("booktype", "BOOKANDNONBOOK")
        ]

        # 해당 구/군에 속한 도서관 코드가 있으면 파라미터 추가
        codes = DISTRICT_LIB_CODES.get(self.region_name, [])
        for c in codes:
            params.append(("libraryCodes", c))

        try:
            resp = requests.get(self.base_url, params=params, headers=self._headers, timeout=15, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 부산도서관 접속 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.content.decode("utf-8", errors="ignore"), "html.parser")

        # 총 건수 추출
        total_count = 0
        total_tag = soup.select_one(".result_total, .search-info, .search-result-text, div.search_result")
        if total_tag:
            m = re.search(r'(\d+)\s*건', total_tag.text)
            if m:
                total_count = int(m.group(1))

        book_items = soup.select("div.bif, ul.sect_lst > li")
        if not total_count:
            total_count = len(book_items)

        if total_count == 0:
            return 0, []

        books = []
        for item in book_items:
            book = BookInfo(region="부산광역시")
            book.library = self.region_name

            # 제목
            title_tag = item.select_one("a.book-title, dt.tit a, span.row_txt_tit a, div.ico a, a.tit")
            if title_tag:
                book.title = title_tag.text.strip()
            else:
                tit_span = item.select_one("span.row_txt_tit, dt.tit")
                if tit_span:
                    book.title = tit_span.text.replace("책제목 :", "").replace("책제목", "").strip()

            full_text = item.get_text(separator="\n", strip=True)

            # 1. 청구기호
            m_call = re.search(r"청구기호\s*[:|\s]*\n*([^\n|]+)", full_text)
            if m_call:
                call_val = m_call.group(1).strip(" |:")
                if call_val and call_val != ":":
                    book.call_number = call_val

            # 2. 저자
            m_author = re.search(r"저자\s*[:|\s]*\n*([^\n|]+)", full_text)
            if m_author:
                auth_val = m_author.group(1).strip(" |:")
                if auth_val and auth_val != ":":
                    book.author = auth_val

            # 3. 소장처 (도서관)
            p_info = item.select_one("p.book-status-info")
            txt_p = p_info.get_text(separator=" | ", strip=True) if p_info else full_text
            m_lib = re.search(r"소장처\s*\|\s*:?\s*\|\s*([^|\n]+?)(?=\s*\||\s*자료실|\s*자료|$)", txt_p) or re.search(r"소장처\s*:?\s*([^|\n]+?)(?=\s*\||\s*자료실|\s*자료|$)", txt_p)
            if m_lib:
                lib_raw = m_lib.group(1).strip(" |:")
                if lib_raw and lib_raw != ":":
                    book.library = lib_raw if "도서관" in lib_raw else lib_raw + "도서관"

            # 4. 자료실
            m_loc = re.search(r"자료실\s*:?\s*(.*?)(?=\s*\||\s*자료|$)", txt_p) or re.search(r"자료실\s*[:|\s]*\n*([^\n|]+)", full_text)
            if m_loc:
                book.location = m_loc.group(1).strip(" |:")

            books.append(book)

        return total_count, books


# 부산광역시 16개 자치구/군 및 주요 도서관 등록
BUSAN_TARGETS = [
    "부산도서관", "부산광역시립시민도서관", "해운대구립도서관", "해운대도서관", "해운대인문학도서관", "금정구립도서관", "사하구립도서관",
    "중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구",
    "해운대구", "기장군", "사하구", "금정구", "강서구", "연제구", "수영구", "사상구"
]

for target_name in set(BUSAN_TARGETS):
    register_scraper(target_name, BusanScraper, metro_name="부산광역시")


