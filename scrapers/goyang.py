"""
고양시 도서관센터 스크래퍼
https://www.goyanglib.or.kr
- 전체 도서관을 대상으로 통합 검색합니다.
- 부록있음/부록없음에 따른 청구기호 파싱 및 음원 여부 처리를 포함합니다.
"""
import re
import requests
from bs4 import BeautifulSoup

from .base import LibraryScraper, BookInfo
from .jnet import _SslAdapter
from .registry import register_scraper


class GoyangScraper(LibraryScraper):
    """고양시 도서관센터 스크래퍼 (www.goyanglib.or.kr)"""

    def __init__(self, region_name="고양시"):
        super().__init__(
            region_name=region_name,
            base_url="https://www.goyanglib.or.kr/center/program/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.goyanglib.or.kr/center/menu/10003/program/30001/searchSimple.do'
        }

        all_books = []
        total_count = 0
        page = 1
        display_num = 100

        while True:
            params = {
                'searchType': 'SIMPLE',
                'searchManageCode': 'ALL',
                'searchKey': 'ALL',
                'searchKeyword': query,
                'currentPageNo': page,
                'searchDisplay': display_num
            }

            try:
                r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')
            except Exception as e:
                print(f"  [오류] 고양시 도서관 검색 실패: {e}")
                return total_count, all_books

            if page == 1:
                total_elem = soup.select_one('.result_screen, .listSetting')
                if total_elem:
                    m = re.search(r'([0-9,]+)\s*건', total_elem.text)
                    if m:
                        total_count = int(m.group(1).replace(',', ''))

            book_areas = soup.select('.bookArea')
            if not book_areas:
                break

            for b in book_areas:
                title_elem = b.select_one('.book_name p.kor a, .book_name a')
                if not title_elem:
                    continue
                raw_title = title_elem.text.strip()
                cleaned_title = re.sub(r'^\s*단행본\s*', '', raw_title).strip()
                cleaned_title = re.sub(r'\s+', ' ', cleaned_title)

                author_elem = b.select_one('.info01 p.kor span, .info01 span')
                b_author = author_elem.text.strip() if author_elem else ""
                b_author = re.sub(r'\s+', ' ', b_author)

                info02_spans = b.select('.info02 p.kor span')
                call_no = ""
                has_audio = ""
                for span in info02_spans:
                    txt = span.text.strip()
                    if txt == '부록있음':
                        has_audio = "O"
                    elif txt == '부록없음':
                        continue
                    else:
                        call_no = txt  # 마지막 non-부록 span이 청구기호
                if not call_no and len(info02_spans) >= 3:
                    call_no = info02_spans[2].text.strip()

                lib_info = b.select_one('.info03 p.kor span, .info03 span')
                lib_text = lib_info.text.strip() if lib_info else ""
                
                m_lib = re.match(r'\[(.*?)\]\s*(.*)', lib_text)
                if m_lib:
                    lib_name = m_lib.group(1).strip()
                    loc_name = m_lib.group(2).strip()
                else:
                    lib_name = lib_text
                    loc_name = ""

                if lib_name and not lib_name.endswith("도서관"):
                    lib_name += "도서관"
                if not lib_name:
                    lib_name = "고양시도서관"

                book = BookInfo(region="경기도")
                book.title = cleaned_title
                book.author = b_author
                book.library = lib_name
                book.location = loc_name
                book.call_number = call_no
                book.has_audio = has_audio
                
                all_books.append(book)

            if total_count == 0:
                total_count = len(all_books)

            if len(all_books) >= total_count or len(book_areas) < display_num:
                break

            page += 1

        return total_count, all_books

register_scraper("고양시", GoyangScraper, metro_name="경기도")
register_scraper("고양시도서관", GoyangScraper, metro_name="경기도")
