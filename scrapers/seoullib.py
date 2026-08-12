"""
서울도서관(대표) LISOS 기반 스크래퍼
- URL: https://lib.seoul.go.kr/main/searchBrief
- 파라미터: st=KWRD, si=TOTAL, sts=Y, searchType=tot, q=검색어
"""
import re
import requests
from bs4 import BeautifulSoup

from .base import LibraryScraper, BookInfo


class SeoulLibScraper(LibraryScraper):
    """서울도서관(대표) LISOS 검색 스크래퍼"""

    def __init__(self):
        super().__init__(
            region_name="서울도서관",
            base_url="https://lib.seoul.go.kr/main/searchBrief"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "st": "KWRD",
            "si": "TOTAL",
            "sts": "Y",
            "searchType": "tot",
            "q": query
        }

        try:
            resp = requests.get(self.base_url, params=params, headers=self._headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 서울도서관 접속 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")

        # 총 건수 - brief.css 구조 상 총 건수는 클래스 .number 등으로 잡히거나 페이징 개수
        # LISOS brief 페이지의 경우 '전체 (N건)' 형태를 띠거나 strong에 표시됨
        total_count = 0
        total_tag = soup.select_one(".sub-title .number")
        if total_tag:
            m = re.search(r'\d+', total_tag.text)
            if m:
                total_count = int(m.group(0))

        book_items = soup.select("ul.list.book-list > li")
        if total_count == 0:
            total_count = len(book_items)

        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            info_div = item.select_one(".info")
            if not info_div:
                continue

            book = BookInfo(region="서울특별시")

            p_tags = info_div.select("p")
            if len(p_tags) >= 1:
                # 1. 제목: 첫 번째 p > a
                title_a = p_tags[0].select_one("a")
                if title_a:
                    book.title = title_a.text.strip()
                else:
                    book.title = p_tags[0].text.strip()

            if len(p_tags) >= 2:
                # 2. 저자: 두 번째 p
                book.author = p_tags[1].text.strip()

            if len(p_tags) >= 4:
                # 4. 청구기호: 네 번째 p
                book.call_number = p_tags[3].text.strip()

            # 도서관/자료실
            loc_tag = item.select_one("p.location > a")
            if loc_tag:
                # '자료실 확인' 버튼 텍스트 제외
                loc_txt = loc_tag.text.strip().replace("도서확인", "").replace("자료확인", "").replace("도서 확인", "").replace("자료 확인", "").replace("도서위치", "").strip()
                book.location = loc_txt
            
            book.library = "서울도서관"

            if book.title:
                books.append(book)

        return total_count, books
