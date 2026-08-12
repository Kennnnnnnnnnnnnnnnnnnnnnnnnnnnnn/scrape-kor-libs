"""
성북구립도서관 전용 실시간 스크래퍼
- URL: https://www.sblib.seoul.kr/library/menu/10012/program/30003/searchResultList.do
- 파라미터: query=검색어, searchField=ALL
"""
import re
import requests
from bs4 import BeautifulSoup

from .base import LibraryScraper, BookInfo
from .jnet import _direct_text, _fetch


class SeongbukScraper(LibraryScraper):
    """성북구립도서관 실시간 검색 스크래퍼 (Type B 변형)"""

    def __init__(self):
        super().__init__(
            region_name="성북구립도서관",
            base_url="https://www.sblib.seoul.kr/library/menu/10012/program/30003/searchResultList.do"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "query": query,
            "searchField": "ALL"
        }

        try:
            resp = _fetch(self.base_url, params, self._headers, use_ssl_adapter=True)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 성북구립도서관 접속 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")

        # 도서 목록
        book_items = soup.select("ul.resultList > li")
        total_count = len(book_items)

        # 총 건수
        total_tag = soup.select_one(".result_screen strong.highlight") or soup.select_one("strong.highlight")
        if total_tag:
            try:
                total_count = int(re.sub(r'[^\d]', '', total_tag.text.strip()))
            except Exception:
                pass

        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            book = BookInfo(region="서울특별시")

            dl = item.select_one("dl.bookDataWrap")
            if not dl:
                continue

            # 1. 제목: dt.tit > a
            title_tag = dl.select_one("dt.tit > a")
            if title_tag:
                raw_title = title_tag.text.strip()
                raw_title = re.sub(r'^\d+\.\s*', '', raw_title)
                book.title = raw_title

            # 2. 저자 및 청구기호 추출
            all_spans = dl.select("dd span")
            for sp in all_spans:
                direct = _direct_text(sp)
                full_txt = sp.text.strip()

                if "저 :" in full_txt or "저자:" in full_txt or "저자 :" in full_txt:
                    book.author = re.sub(r'^(?:저자?\s*:\s*|저\s*:\s*)', '', full_txt).strip()

                if "청구기호" in direct or "청구번호" in direct or "청구" in direct:
                    call_match = re.search(r'(?:청구기호|청구번호|청구)\s*:\s*(.+)', direct)
                    if call_match:
                        book.call_number = call_match.group(1).strip()
                    else:
                        book.call_number = direct.replace("청구기호", "").replace("청구번호", "").replace("청구", "").replace(":", "").strip()

            # 3. 소장 도서관 및 자료실
            site_dd = dl.select_one("dd.site")
            if site_dd:
                spans = site_dd.select("span")
                for sp in spans:
                    txt = sp.text.strip()
                    if "소장" in txt or "도서관" in txt:
                        lib_name = re.sub(r'^(?:소장\s*:\s*|도서관\s*:\s*)', '', txt).strip()
                        book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                    elif "자료실" in txt or "위치" in txt:
                        loc = re.sub(r'^(?:자료실\s*:\s*|위치\s*:\s*)', '', txt).strip()
                        book.location = loc

            if not book.library:
                # location에서 유추
                if book.location and "[" in book.location and "]" in book.location:
                    m = re.search(r'\[(.+?)\]', book.location)
                    if m:
                        book.library = m.group(1) + "도서관"
                else:
                    book.library = "성북구립도서관"
            
            if "도서관도서관" in book.library:
                book.library = book.library.replace("도서관도서관", "도서관")

            if book.title:
                books.append(book)

        return total_count, books
