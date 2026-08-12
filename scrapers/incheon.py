import re
import requests
from bs4 import BeautifulSoup
from .base import LibraryScraper, BookInfo
from .registry import register_scraper
from .generic import GenericLibraryScraper
from .gyeonggi import _SslAdapter


import re
import requests
from bs4 import BeautifulSoup
from .base import LibraryScraper, BookInfo
from .registry import register_scraper
from .generic import GenericLibraryScraper
from .gyeonggi import _SslAdapter


class IncheonEducationScraper(LibraryScraper):
    """인천광역시교육청 통합도서관 스크래퍼 (lib.ice.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="인천광역시교육청도서관",
            base_url="https://lib.ice.go.kr/ice/intro/search/index.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menu_idx": "113",
            "booktype": "BOOK",
            "search_type": "L_TITLE",
            "search_text": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.ice.go.kr/ice/index.do'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 인천광역시교육청도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        # 총 건수 추출
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        # 도서 목록 추출
        items = soup.select("div.bif")
        books = []
        for item in items:
            txt = item.text.strip().replace("\n", " ")
            lines = [l.strip() for l in item.text.split("\n") if l.strip()]
            book_title = lines[0] if lines else ""

            if not book_title:
                continue

            m_auth = re.search(r"저자명\s*:\s*([^발행자|소장처|청구기호]+)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"소장처\s*:\s*([^/\n]+)", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "인천광역시교육청도서관"

            m_loc = re.search(r"/\s*(\[[^\]]+\][^\n]+)", txt)
            location = m_loc.group(1).strip() if m_loc else ""

            m_call = re.search(r"청구기호\s*:\s*([^\s]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="인천광역시")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.location = location
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("인천광역시교육청도서관", IncheonEducationScraper, metro_name="인천광역시")
register_scraper("미추홀도서관", IncheonEducationScraper, metro_name="인천광역시")
register_scraper("부평구립도서관", IncheonEducationScraper, metro_name="인천광역시")
register_scraper("연수구립도서관", IncheonEducationScraper, metro_name="인천광역시")

