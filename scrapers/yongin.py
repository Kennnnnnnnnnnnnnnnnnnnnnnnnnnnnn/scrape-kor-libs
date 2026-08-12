"""
용인시립도서관 스크래퍼
https://lib.yongin.go.kr
"""
import requests
import re
from bs4 import BeautifulSoup
from .base import LibraryScraper, BookInfo
from .registry import register_scraper
from .jnet import _SslAdapter

class YonginScraper(LibraryScraper):
    """용인시립도서관 도서 검색"""

    def __init__(self):
        super().__init__(
            region_name="용인시",
            base_url="https://lib.yongin.go.kr/yongin/menu/10181/program/30012/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.yongin.go.kr/'
        }
        params = {
            "searchType": "SIMPLE",
            "searchCategory": "BOOK",
            "searchKey": "TITLE",
            "searchKeyword": query,
            "searchOrder": "DESC",
            "searchManageCode": "ALL",
            "searchDisplay": "100"
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            print(f"  [오류] 용인시 도서관 검색 실패: {e}")
            return 0, []

        book_areas = soup.select(".bookArea") or soup.select("ul.resultList > li")
        if not book_areas:
            return 0, []

        books = []
        for item in book_areas:
            book = BookInfo(region="경기도")
            title_tag = item.select_one(".book_name a, a.book_name, .book_name, dt.tit > a")
            if title_tag:
                raw_title = re.sub(r'^\s*단행본\s*', '', title_tag.text.strip())
                raw_title = re.sub(r'^\s*도서\s*', '', raw_title).strip()
                book.title = raw_title
            
            author_sp = item.select_one(".info01 p.kor span, .info01 span")
            if author_sp:
                book.author = author_sp.text.strip()
            
            info02_spans = item.select(".info02 p.kor span, .info02 span")
            if len(info02_spans) >= 3:
                book.call_number = info02_spans[2].text.strip()
            elif len(info02_spans) == 2:
                book.call_number = info02_spans[1].text.strip()

            lib_sp = item.select_one(".info03 p.kor span, .info03 span")
            if lib_sp:
                txt = lib_sp.text.strip()
                m = re.match(r'\[(.*?)\]\s*(.*)', txt)
                if m:
                    book.library = m.group(1).strip()
                    book.location = m.group(2).strip()
                else:
                    book.library = txt

            if not book.library:
                book.library = "용인시도서관"
            if book.title:
                books.append(book)

        return len(books), books

register_scraper("용인", YonginScraper)
register_scraper("용인시", YonginScraper)
register_scraper("용인시립도서관", YonginScraper)
