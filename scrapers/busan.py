"""
부산도서관 스크래퍼
https://library.busan.go.kr
"""
import re
import requests
from bs4 import BeautifulSoup

from .base import LibraryScraper, BookInfo
from .registry import register_scraper


class BusanScraper(LibraryScraper):
    """부산도서관 도서 검색"""

    def __init__(self):
        super().__init__(
            region_name="부산도서관",
            base_url="https://library.busan.go.kr/busanlibrary/intro/totalSearch/book.do"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        search_kw = f"{title} {author}".strip() if author else title
        params = {
            "search_text": search_kw
        }

        try:
            resp = requests.get(self.base_url, params=params, headers=self._headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 부산도서관 접속 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.content.decode("utf-8", errors="ignore"), "html.parser")

        # 총 건수
        total_tag = soup.select_one(".result_total")
        total_count = 0
        if total_tag:
            m = re.search(r'\d+', total_tag.text)
            if m:
                total_count = int(m.group(0))

        if total_count == 0:
            return 0, []

        books = []
        book_items = soup.select("ul.sect_lst > li")

        for item in book_items:
            book = BookInfo(region="부산광역시")

            # 제목
            title_tag = item.select_one("span.row_txt_tit a")
            if title_tag:
                book.title = title_tag.text.strip()
            else:
                tit_span = item.select_one("span.row_txt_tit")
                if tit_span:
                    book.title = tit_span.text.replace("책제목 :", "").replace("책제목", "").strip()

            # 저자 / 청구기호 / 자료이용장소
            spans = item.select("span")
            for sp in spans:
                txt = sp.text.strip()
                if "저자 :" in txt or txt.startswith("저자"):
                    book.author = txt.replace("저자 :", "").replace("저자", "").strip()
                elif "청구기호 :" in txt or txt.startswith("청구기호"):
                    book.call_number = txt.replace("청구기호 :", "").replace("청구기호", "").strip()
                elif "자료이용장소 :" in txt or txt.startswith("자료이용장소"):
                    loc_text = txt.replace("자료이용장소 :", "").replace("자료이용장소", "").strip()
                    book.location = loc_text

                    # 도서관명 추출
                    match = re.search(r'\[(.+?)\]', loc_text)
                    if match:
                        lib_base = match.group(1).strip()
                        book.library = lib_base if lib_base.endswith("도서관") else lib_base + "도서관"
                    else:
                        book.library = "부산도서관"

            if not book.library:
                book.library = "부산도서관"

            books.append(book)

        return total_count, books


register_scraper("부산도서관", BusanScraper, metro_name="부산광역시")
