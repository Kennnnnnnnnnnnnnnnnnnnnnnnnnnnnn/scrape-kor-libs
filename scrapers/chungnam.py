"""충청남도 도서관 스크래퍼 모듈 (scrapers/chungnam.py)
천안시도서관, 아산시립도서관, 충청남도도서관, 논산시립도서관 전용 스크래퍼
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
# 충남 아산시립도서관 (lib.asan.go.kr DLS 종이도서관 & elib.asan.go.kr 전자도서관)
# ========================================================================

class AsanScraper(LibraryScraper):
    """충남 아산시립도서관 스크래퍼 (lib.asan.go.kr & elib.asan.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="아산시립도서관",
            base_url="https://lib.asan.go.kr/dls_le/index.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        books = []
        seen = set()
        total_count = 0

        # 1. 아산시립 종이도서관 (DLS) 수집
        headers_dls = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://ascl.asan.go.kr/index.php'
        }
        params_dls = {
            "mod": "wdDataSearch",
            "act": "searchIList",
            "item": "total",
            "word": query,
            "manageCode": "",
            "page": 1
        }

        try:
            r = self._session.get(self.base_url, params=params_dls, headers=headers_dls, timeout=12, verify=False)
            r.raise_for_status()
            soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")

            settype_tag = soup.select_one("div.settype, span.total, div.total")
            search_txt = settype_tag.get_text(strip=True) if settype_tag else soup.text
            m = re.search(r'총\s*(\d+)\s*건', search_txt) or re.search(r'(\d+)\s*건', search_txt)
            if m:
                total_count = int(m.group(1))

            def _parse_page_items(page_soup):
                items = page_soup.select("div.divList > div.list")
                for item in items:
                    book_title = ""
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
                    lib_name = lib_el.get_text(strip=True) if lib_el else "아산시립도서관"

                    m_call = re.search(r"청구기호\s*:?\s*([^|\n]+?)(?=\s*등록번호|\s*소장|\s*대출|\s*자료|$)", txt)
                    call_no = m_call.group(1).strip() if m_call else ""

                    status_el = item.select_one("ol strong")
                    status_text = status_el.get_text(strip=True) if status_el else ""
                    is_available = ("대출가능" in status_text) or ("가능" in status_text) or ("대출가능" in txt)

                    key = (book_title, book_author, lib_name, call_no)
                    if key in seen:
                        continue
                    seen.add(key)

                    book = BookInfo(region="충청남도")
                    book.title = book_title
                    book.author = book_author
                    book.library = lib_name if lib_name else "아산시립도서관"
                    book.call_number = call_no
                    book.available = is_available
                    books.append(book)

            _parse_page_items(soup)

            # Fetch remaining pages for DLS paper books
            if total_count > 10:
                total_pages = min((total_count + 9) // 10, 10)
                for p in range(2, total_pages + 1):
                    try:
                        p_params = {**params_dls, "page": p}
                        pr = self._session.get(self.base_url, params=p_params, headers=headers_dls, timeout=8, verify=False)
                        if pr.status_code == 200:
                            p_soup = BeautifulSoup(pr.content.decode('utf-8', 'ignore'), "html.parser")
                            _parse_page_items(p_soup)
                    except Exception:
                        pass
        except Exception as e:
            print(f"  [오류] 아산시립 종이도서관 DLS 검색 실패: {e}")

        # 2. 아산시 전자도서관 (Elib) 병행 수집
        try:
            url_elib = "https://elib.asan.go.kr/elibrary-front/search/searchList.ink"
            params_elib = {
                'schClst': 'all',
                'schDvsn': '000',
                'orderByKey': '',
                'schTxt': query
            }
            headers_elib = {
                'User-Agent': self._headers['User-Agent'],
                'Referer': 'https://elib.asan.go.kr/elibrary-front/'
            }
            r_e = self._session.get(url_elib, params=params_elib, headers=headers_elib, timeout=10, verify=False)
            if r_e.status_code == 200:
                soup_e = BeautifulSoup(r_e.content.decode('utf-8', 'ignore'), "html.parser")
                items_e = soup_e.select("ul.book_resultList > li")
                for item in items_e:
                    tit_tag = item.select_one("li.tit a, li.tit, a.title")
                    b_title = tit_tag.get_text(strip=True) if tit_tag else ""
                    b_title = re.sub(r'<[^>]+>', '', b_title).strip()
                    if not b_title:
                        continue

                    writer_tag = item.select_one("li.writer, span.writer")
                    b_author = writer_tag.get_text(strip=True) if writer_tag else ""

                    key = (b_title, b_author, "아산시전자도서관", "")
                    if key in seen:
                        continue
                    seen.add(key)

                    book = BookInfo(region="충청남도")
                    book.title = b_title
                    book.author = b_author
                    book.library = "아산시전자도서관"
                    book.available = True
                    books.append(book)
        except Exception:
            pass

        final_total = max(total_count, len(books))
        return final_total, books


# ========================================================================
# 충남 천안시도서관 (kolas.cheonan.go.kr & elib.cheonan.go.kr)
# ========================================================================

class CheonanScraper(LibraryScraper):
    """충남 천안시도서관 스크래퍼 (kolas.cheonan.go.kr & elib.cheonan.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="천안시도서관",
            base_url="https://kolas.cheonan.go.kr/search/index.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        books = []
        total_count = 0

        params_k = {
            "mod": "wdDataSearch",
            "act": "searchIList",
            "item": "total",
            "word": query,
            "manageCode": ""
        }
        headers_k = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://kolas.cheonan.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params_k, headers=headers_k, timeout=12, verify=False)
            r.raise_for_status()
            soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")

            cnt_tag = soup.select_one("span.total, span.num, strong.count, div.total")
            if cnt_tag:
                m = re.search(r"\d+", cnt_tag.text.strip())
                if m:
                    total_count = int(m.group(0))

            items = soup.select("div.divList > div.list")
            for item in items:
                tit_tag = item.select_one("div.ico a") or item.select_one("dt a") or item.select_one("a[href*='searchResultDetail']")
                book_title = ""
                if tit_tag:
                    book_title = tit_tag.get_text(strip=True)
                    if not book_title and tit_tag.find('img'):
                        book_title = tit_tag.find('img').get('alt', '')

                book_title = re.sub(r'<[^>]+>', '', book_title).strip()
                if not book_title:
                    txt_full = item.text.strip()
                    lines = [l.strip() for l in txt_full.split("\n") if l.strip()]
                    book_title = lines[0] if lines else ""

                if not book_title:
                    continue

                txt = item.text.strip().replace("\n", " ")

                lib_el = item.select_one("li.so span.blue") or item.select_one("li.so span")
                lib_name = lib_el.get_text(strip=True) if lib_el else "천안시도서관"

                m_call = re.search(r"청구기호\s*:?\s*([^|\n]+?)(?=\s*등록번호|\s*소장|\s*대출|\s*자료|$)", txt)
                call_no = m_call.group(1).strip() if m_call else ""

                status_el = item.select_one("ol strong")
                status_text = status_el.get_text(strip=True) if status_el else ""
                is_available = ("대출가능" in status_text) or ("가능" in status_text)

                book = BookInfo(region="충청남도")
                book.title = book_title
                book.library = lib_name if lib_name else "천안시도서관"
                book.call_number = call_no
                book.available = is_available
                books.append(book)
        except Exception as e:
            print(f"  [오류] 천안시도서관 KOLAS 검색 실패: {e}")

        # FxLibrary (전자도서관) - 병행 수집
        try:
            url_e = "https://elib.cheonan.go.kr/FxLibrary/product/list/"
            params_e = {
                'category': 'book',
                'searchoption': '1',
                'searchType': 'search',
                'keyword': query
            }
            headers_e = {
                'User-Agent': self._headers['User-Agent'],
                'Referer': 'https://elib.cheonan.go.kr/FxLibrary/'
            }
            r_e = self._session.get(url_e, params=params_e, headers=headers_e, timeout=10, verify=False)
            if r_e.status_code == 200:
                soup_e = BeautifulSoup(r_e.content.decode('utf-8', 'ignore'), "html.parser")
                e_items = soup_e.select(".book_list li, div.book_box, ul.list_type_box > ul > li")
                for item in e_items:
                    tit_tag = item.select_one(".title, a.book_title, dt a, p.tit")
                    if tit_tag:
                        b_title = tit_tag.get_text(strip=True)
                        b_title = re.sub(r'<[^>]+>', '', b_title).strip()
                        if b_title:
                            book = BookInfo(region="충청남도")
                            book.title = b_title
                            book.library = "천안시전자도서관"
                            book.available = True
                            books.append(book)
        except Exception:
            pass

        final_total = max(total_count, len(books))
        return final_total, books


# ========================================================================
# 충청남도도서관 (cdlib.chungnam.go.kr)
# ========================================================================

class ChungnamDolibScraper(LibraryScraper):
    """충청남도도서관 스크래퍼 (cdlib.chungnam.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="충청남도도서관",
            base_url="https://cdlib.chungnam.go.kr/search/searchResult.do"
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
            'Referer': 'https://cdlib.chungnam.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 충청남도도서관 검색 실패: {e}")
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

            book = BookInfo(region="충청남도")
            book.title = book_title
            book.author = book_author
            book.library = "충청남도도서관"
            book.available = ("대출가능" in txt) or ("가능" in txt)
            books.append(book)

        return total_count if total_count > 0 else len(books), books


# ========================================================================
# 충남 논산시립도서관 (lib.nonsan.go.kr)
# ========================================================================

class NonsanScraper(LibraryScraper):
    """충남 논산시립도서관 스크래퍼 (lib.nonsan.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="논산시립도서관",
            base_url="https://lib.nonsan.go.kr/search/searchResult.do"
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
            'Referer': 'https://lib.nonsan.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 논산시립도서관 검색 실패: {e}")
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

            book = BookInfo(region="충청남도")
            book.title = book_title
            book.author = book_author
            book.library = "논산시립도서관"
            book.available = ("대출가능" in txt) or ("가능" in txt)
            books.append(book)

        return total_count if total_count > 0 else len(books), books


# ========================================================================
# 충청남도 도서관 레지스트리 등록
# ========================================================================

for name in ["아산시립도서관", "아산시도서관", "아산도서관", "아산시전자도서관", "아산전자도서관"]:
    register_scraper(name, AsanScraper, metro_name="충청남도")

for name in ["천안시도서관", "천안시립도서관", "천안도서관", "천안시전자도서관", "천안전자도서관"]:
    register_scraper(name, CheonanScraper, metro_name="충청남도")

for name in ["충청남도도서관", "충남도서관"]:
    register_scraper(name, ChungnamDolibScraper, metro_name="충청남도")

for name in ["논산시립도서관", "논산시도서관", "논산도서관"]:
    register_scraper(name, NonsanScraper, metro_name="충청남도")
