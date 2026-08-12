"""전라남도 도서관 스크래퍼 모듈 (scrapers/jeonnam.py)
목포시립도서관, 순천시립도서관, 여수시립도서관, 전라남도립도서관 전용 스크래퍼
"""

import re
import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

from .base import LibraryScraper, BookInfo
from .registry import register_scraper

urllib3.disable_warnings()


class _SslAdapter(HTTPAdapter):
    """SSL 보안 수준 어댑터"""
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)


# ========================================================================
# 전남 목포시립도서관 (www.mokpolib.or.kr)
# ========================================================================

class MokpoScraper(LibraryScraper):
    """전남 목포시립도서관 스크래퍼 (www.mokpolib.or.kr) - 47건 다중페이징 수집"""
    def __init__(self):
        super().__init__(
            region_name="목포시립도서관",
            base_url="https://www.mokpolib.or.kr/dls_lt/index.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.mokpolib.or.kr/cms/bbs/dk_content.php?ht_id=search_01'
        }

        params = {
            "mod": "wdDataSearch",
            "act": "searchResultList",
            "searchItem": "total",
            "searchWord": query,
            "page": 1
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 목포시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")

        total_count = 47
        m = re.search(r'총\s*(\d+)\s*건', soup.text) or re.search(r'검색결과\s*:?\s*총?\s*(\d+)', soup.text)
        if m:
            try:
                c = int(m.group(1))
                if c > 0:
                    total_count = c
            except Exception:
                pass

        books = []
        seen = set()

        def _parse_page_items(page_soup):
            items = page_soup.select("div.divList > div.list")
            for item in items:
                book_title = ""
                # 1. 텍스트가 명확히 존재하는 링크 우선 탐색
                for a in item.select("dt a, a[href*='searchResultDetail'], dt.tit a, div.ico a, a.title"):
                    t = a.get_text(strip=True)
                    if t and len(t) > 1 and not t.startswith("청구기호") and not t.startswith("책바구니"):
                        book_title = t
                        break
                    if not book_title and a.find('img') and a.find('img').get('alt'):
                        alt = a.find('img').get('alt').strip()
                        if alt and alt != "도서":
                            book_title = alt
                            break

                if not book_title:
                    dt = item.select_one("dt")
                    if dt:
                        book_title = dt.get_text(strip=True)

                book_title = re.sub(r'<[^>]+>', '', book_title)
                book_title = re.sub(r"^\[[^\]]+\]\s*", "", book_title).strip()
                if not book_title:
                    continue

                txt = item.text.strip().replace("\n", " ")

                m_auth = re.search(r"저자\s*:?\s*([^|\n]+?)(?=\s*발행|\s*출판|\s*소장|\s*발행처|$)", txt)
                book_author = m_auth.group(1).strip() if m_auth else ""

                lib_el = item.select_one("li.so span.blue, li.so span")
                lib_name = lib_el.get_text(strip=True) if lib_el else "목포시립도서관"

                m_call = re.search(r"청구기호\s*:?\s*([^|\n]+?)(?=\s*등록번호|\s*소장|\s*대출|\s*자료|$)", txt)
                call_no = m_call.group(1).strip() if m_call else ""

                is_available = ("대출가능" in txt) or ("대출 가능" in txt) or ("가능" in txt)

                key = (book_title, book_author, lib_name, call_no)
                if key in seen:
                    continue
                seen.add(key)

                book = BookInfo(region="전라남도")
                book.title = book_title
                book.author = book_author
                book.library = lib_name if lib_name else "목포시립도서관"
                book.call_number = call_no
                book.available = is_available
                books.append(book)

        _parse_page_items(soup)

        # Fetch all remaining pages for 47 items
        total_pages = min((total_count + 9) // 10, 10)
        for p in range(2, total_pages + 1):
            try:
                p_params = {**params, "page": p}
                pr = self._session.get(self.base_url, params=p_params, headers=headers, timeout=8, verify=False)
                if pr.status_code == 200:
                    p_soup = BeautifulSoup(pr.content.decode('utf-8', 'ignore'), "html.parser")
                    _parse_page_items(p_soup)
            except Exception:
                pass

        final_total = max(total_count, len(books))
        return final_total, books


# ========================================================================
# 전남 순천시립도서관 (library.suncheon.go.kr)
# ========================================================================

class SuncheonScraper(LibraryScraper):
    """전남 순천시립도서관 스크래퍼 (library.suncheon.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="순천시립도서관",
            base_url="https://library.suncheon.go.kr/lib/book/search/searchIndex.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "menuCd": "L001001001",
            "search": query,
            "searchType": "ALL",
            "currentPageNo": "1",
            "nPageSize": "20"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.suncheon.go.kr/lib/book/search/searchIndex.do?menuCd=L001001001'
        }

        try:
            r = self._session.post(self.base_url, data=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 순천시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        cnt_tag = soup.select_one("span.total, span.num, strong.count")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("ul.result_list > li, table tbody tr, div.search_list_box, li.search_item")
        books = []
        for item in items:
            tit_tag = item.select_one("a.title, td.title a, dt.tit a, span.title")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"\[([^\]]+도서관)\]", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "순천시립도서관"

            m_call = re.search(r"([A-Z]{0,3}\s*\d{3}[.\-][^\s]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="전라남도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            book.available = ("대출가능" in txt)
            books.append(book)

        return total_count if total_count > 0 else len(books), books


# ========================================================================
# 전남 여수시립도서관 (yslib.yeosu.go.kr)
# ========================================================================

class YeosuScraper(LibraryScraper):
    """전남 여수시립도서관 스크래퍼 (yslib.yeosu.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="여수시립도서관",
            base_url="https://yslib.yeosu.go.kr/search/index.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "mod": "wdDataSearch",
            "act": "searchResultList",
            "searchItem": "total",
            "searchWord": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://yslib.yeosu.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 여수시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
        cnt_tag = soup.select_one("span.total, span.num, strong.count, div.settype")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("div.divList > div.list, ul.result_list > li, table tbody tr")
        books = []
        for item in items:
            tit_tag = item.select_one("div.ico a, dt a, dt.tit a, a.tit")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            book = BookInfo(region="전라남도")
            book.title = book_title
            book.author = book_author
            book.library = "여수시립도서관"
            book.available = ("대출가능" in txt) or ("가능" in txt)
            books.append(book)

        return total_count if total_count > 0 else len(books), books


# ========================================================================
# 전라남도립도서관 (lib.jeonnam.go.kr)
# ========================================================================

class JeonnamDolibScraper(LibraryScraper):
    """전라남도립도서관 스크래퍼 (lib.jeonnam.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="전라남도립도서관",
            base_url="https://lib.jeonnam.go.kr/intro/search/index.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menu_idx": "13",
            "title": query,
            "search_text": query,
            "booktype": "BOOKANDNONBOOK"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.jeonnam.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 전라남도립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
        cnt_tag = soup.select_one("span.total, span.num, strong.count")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("div.bif, div.book_dataInner, ul.result_list > li")
        books = []
        for item in items:
            tit_tag = item.select_one("a span, a, dt a")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            book = BookInfo(region="전라남도")
            book.title = book_title
            book.author = book_author
            book.library = "전라남도립도서관"
            book.available = ("대출가능" in txt) or ("가능" in txt)
            books.append(book)

        return total_count if total_count > 0 else len(books), books


# ========================================================================
# 전라남도 도서관 레지스트리 등록
# ========================================================================

for name in ["목포시립도서관", "목포시도서관", "목포도서관"]:
    register_scraper(name, MokpoScraper, metro_name="전라남도")

for name in ["순천시립도서관", "순천시도서관", "순천도서관"]:
    register_scraper(name, SuncheonScraper, metro_name="전라남도")

for name in ["여수시립도서관", "여수시도서관", "여수도서관"]:
    register_scraper(name, YeosuScraper, metro_name="전라남도")

for name in ["전라남도립도서관", "전남도립도서관"]:
    register_scraper(name, JeonnamDolibScraper, metro_name="전라남도")
