"""
제주특별자치도 공공도서관 스크래퍼 (통합 및 16개 도서관 개별 지원)
https://www.jeju.go.kr/tool/lib/search.jsp
"""
import requests
from .base import LibraryScraper, BookInfo
from .registry import register_scraper

JEJU_LIB_MAP = {
    'MJ': '한라도서관',
    'MK': '우당도서관',
    'ML': '탐라도서관',
    'MM': '제주시기적의도서관',
    'MP': '애월도서관',
    'MN': '조천읍도서관',
    'MQ': '한경도서관',
    'MA': '삼매봉도서관',
    'MB': '중앙도서관',
    'MC': '동부도서관',
    'MD': '서부도서관',
    'ME': '서귀포기적의도서관',
    'MH': '성산일출도서관',
    'MF': '안덕산방도서관',
    'MG': '표선도서관',
    'XY': '꿈바당어린이도서관',
}

NAME_TO_CODE = {v: k for k, v in JEJU_LIB_MAP.items()}


class JejuScraper(LibraryScraper):
    """제주 공공도서관 도서 검색"""

    def __init__(self, target_lib_name: str = "제주도립도서관"):
        super().__init__(
            region_name=target_lib_name,
            base_url="https://www.jeju.go.kr/tool/lib/search.jsp"
        )
        self.target_lib_name = target_lib_name
        self.target_manage_code = NAME_TO_CODE.get(target_lib_name, None)

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {"q": query}
        if self.target_manage_code:
            params["mCode"] = self.target_manage_code

        try:
            resp = requests.get(self.base_url, params=params, headers=self._headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  [오류] 제주 도서관 접속 실패: {e}")
            return 0, []

        book_list = data.get("books", [])
        if not book_list:
            return 0, []

        books = []
        for item in book_list:
            m_code = item.get("manageCode", "")
            
            if self.target_manage_code and m_code != self.target_manage_code:
                continue

            lib_name = JEJU_LIB_MAP.get(m_code, "제주공공도서관")

            class_no = item.get("classNo", "") or ""
            book_code = item.get("bookCode", "") or ""
            call_no = f"{class_no} {book_code}".strip()

            location = item.get("idxHoldPlace", "") or ""

            book = BookInfo(
                title=item.get("title", "") or "",
                author=item.get("author", "") or "",
                region="제주특별자치도",
                library=lib_name,
                location=location,
                call_number=call_no,
                has_audio=""
            )
            books.append(book)

        return len(books), books


# 제주도립도서관 (전체 통합 검색)
register_scraper("제주도립도서관", JejuScraper, metro_name="제주특별자치도")


class JejuMJScraper(JejuScraper):
    def __init__(self): super().__init__('한라도서관')

class JejuMKScraper(JejuScraper):
    def __init__(self): super().__init__('우당도서관')

class JejuMLScraper(JejuScraper):
    def __init__(self): super().__init__('탐라도서관')

class JejuMMScraper(JejuScraper):
    def __init__(self): super().__init__('제주시기적의도서관')

class JejuMPScraper(JejuScraper):
    def __init__(self): super().__init__('애월도서관')

class JejuMNScraper(JejuScraper):
    def __init__(self): super().__init__('조천읍도서관')

class JejuMQScraper(JejuScraper):
    def __init__(self): super().__init__('한경도서관')

class JejuMAScraper(JejuScraper):
    def __init__(self): super().__init__('삼매봉도서관')

class JejuMBScraper(JejuScraper):
    def __init__(self): super().__init__('중앙도서관')

class JejuMCScraper(JejuScraper):
    def __init__(self): super().__init__('동부도서관')

class JejuMDScraper(JejuScraper):
    def __init__(self): super().__init__('서부도서관')

class JejuMEScraper(JejuScraper):
    def __init__(self): super().__init__('서귀포기적의도서관')

class JejuMHScraper(JejuScraper):
    def __init__(self): super().__init__('성산일출도서관')

class JejuMFScraper(JejuScraper):
    def __init__(self): super().__init__('안덕산방도서관')

class JejuMGScraper(JejuScraper):
    def __init__(self): super().__init__('표선도서관')

class JejuXYScraper(JejuScraper):
    def __init__(self): super().__init__('꿈바당어린이도서관')


register_scraper('한라도서관', JejuMJScraper, metro_name="제주특별자치도")
register_scraper('우당도서관', JejuMKScraper, metro_name="제주특별자치도")
register_scraper('탐라도서관', JejuMLScraper, metro_name="제주특별자치도")
register_scraper('제주시기적의도서관', JejuMMScraper, metro_name="제주특별자치도")
register_scraper('애월도서관', JejuMPScraper, metro_name="제주특별자치도")
register_scraper('조천읍도서관', JejuMNScraper, metro_name="제주특별자치도")
register_scraper('한경도서관', JejuMQScraper, metro_name="제주특별자치도")
register_scraper('삼매봉도서관', JejuMAScraper, metro_name="제주특별자치도")
register_scraper('중앙도서관', JejuMBScraper, metro_name="제주특별자치도")
register_scraper('동부도서관', JejuMCScraper, metro_name="제주특별자치도")
register_scraper('서부도서관', JejuMDScraper, metro_name="제주특별자치도")
register_scraper('서귀포기적의도서관', JejuMEScraper, metro_name="제주특별자치도")
register_scraper('성산일출도서관', JejuMHScraper, metro_name="제주특별자치도")
register_scraper('안덕산방도서관', JejuMFScraper, metro_name="제주특별자치도")
register_scraper('표선도서관', JejuMGScraper, metro_name="제주특별자치도")
register_scraper('꿈바당어린이도서관', JejuXYScraper, metro_name="제주특별자치도")
