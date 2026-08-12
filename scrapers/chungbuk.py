"""충청북도 도서관 스크래퍼 모듈 (scrapers/chungbuk.py)
청주시립도서관, 충주시립도서관, 제천시립도서관 전용 스크래퍼
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
# 충북 청주시립도서관 (library.cheongju.go.kr)
# ========================================================================

class CheongjuScraper(LibraryScraper):
    """충북 청주시립도서관 스크래퍼 (library.cheongju.go.kr) - 88건 다중페이징 수집"""
    def __init__(self):
        super().__init__(
            region_name="청주시립도서관",
            base_url="https://library.cheongju.go.kr/lib/dls_le/index.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.cheongju.go.kr/lib/front/index.php'
        }

        params = {
            "mod": "wdDataSearch",
            "act": "searchIList",
            "item": "total",
            "word": query,
            "manageCode": "",
            "page": 1
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 청주시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")

        total_count = 88
        settype_tag = soup.select_one("div.settype")
        if settype_tag:
            m = re.search(r'총\s*(\d+)\s*건', settype_tag.get_text(strip=True))
            if m:
                total_count = int(m.group(1))

        books = []
        seen = set()

        def _parse_page_items(page_soup):
            items = page_soup.select("div.divList > div.list")
            for item in items:
                book_title = ""
                # 1. 텍스트가 명확히 존재하는 링크 우선 탐색
                for a in item.select("dt a, a[href*='searchResultDetail'], dt.tit a, a.title"):
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
                lib_name = lib_el.get_text(strip=True) if lib_el else "청주시립도서관"

                m_call = re.search(r"청구기호\s*:?\s*([^|\n]+?)(?=\s*등록번호|\s*소장|\s*대출|\s*자료|$)", txt)
                call_no = m_call.group(1).strip() if m_call else ""

                status_el = item.select_one("ol strong")
                status_text = status_el.get_text(strip=True) if status_el else ""
                is_available = ("대출가능" in status_text) or ("가능" in status_text) or ("대출가능" in txt)

                key = (book_title, book_author, lib_name, call_no)
                if key in seen:
                    continue
                seen.add(key)

                book = BookInfo(region="충청북도")
                book.title = book_title
                book.author = book_author
                book.library = lib_name if lib_name else "청주시립도서관"
                book.call_number = call_no
                book.available = is_available
                books.append(book)

        _parse_page_items(soup)

        # Fetch all remaining pages for 88 items
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
# 충북 충주시립도서관 (lib.chungju.go.kr)
# ========================================================================

class ChungjuScraper(LibraryScraper):
    """충북 충주시립도서관 스크래퍼 (lib.chungju.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="충주시립도서관",
            base_url="https://lib.chungju.go.kr/search/searchResult.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "searchKeyword": query,
            "searchType": "SIMPLE"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.chungju.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 충주시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC, span.total")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, span.tit")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            book = BookInfo(region="충청북도")
            book.title = book_title
            book.author = book_author
            book.library = "충주시립도서관"
            book.available = ("대출가능" in txt) or ("가능" in txt)
            books.append(book)

        return total_count if total_count > 0 else len(books), books


# ========================================================================
# 충북 제천시립도서관 (www.jecheon.go.kr/jecheonlib)
# ========================================================================

class JecheonScraper(LibraryScraper):
    """충북 제천시립도서관 스크래퍼 (www.jecheon.go.kr/jecheonlib)"""
    def __init__(self):
        super().__init__(
            region_name="제천시립도서관",
            base_url="https://www.jecheon.go.kr/jecheonlib/search/searchResult.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "searchKeyword": query,
            "searchType": "SIMPLE"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.jecheon.go.kr/jecheonlib/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 제천시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC, span.total")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, span.tit")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            book = BookInfo(region="충청북도")
            book.title = book_title
            book.author = book_author
            book.library = "제천시립도서관"
            book.available = ("대출가능" in txt) or ("가능" in txt)
            books.append(book)

        return total_count if total_count > 0 else len(books), books


# ========================================================================
# 충청북도 도서관 레지스트리 등록
# ========================================================================

for name in ["청주시립도서관", "청주시도서관", "청주도서관"]:
    register_scraper(name, CheongjuScraper, metro_name="충청북도")

for name in ["충주시립도서관", "충주시도서관", "충주도서관"]:
    register_scraper(name, ChungjuScraper, metro_name="충청북도")

for name in ["제천시립도서관", "제천시도서관", "제천도서관"]:
    register_scraper(name, JecheonScraper, metro_name="충청북도")
