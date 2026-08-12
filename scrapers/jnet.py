"""
jnet CMS 기반 공공도서관 통합 스크래퍼
- Type A: searchResultList.do (#totalCnt + #bookList 패턴)
- Type B: plusSearchResultList.do (ul.resultList + dl.bookDataWrap 패턴)
"""
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from bs4 import BeautifulSoup, NavigableString

from .base import LibraryScraper, BookInfo

# 구형 SSL 사이트용 어댑터
_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'


class _SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        kwargs['ssl_context'] = ctx
        return super().proxy_manager_for(*args, **kwargs)


def _parse_int(text: str) -> int:
    """숫자 문자열에서 쉼표 등을 제거하고 정수로 변환합니다."""
    if not text:
        return 0
    cleaned = re.sub(r'[^\d]', '', text.strip())
    return int(cleaned) if cleaned else 0


def _direct_text(tag) -> str:
    """태그의 직접 텍스트만 추출합니다 (자식 태그 텍스트 제외)."""
    if not tag:
        return ""
    return ''.join(
        child.strip() for child in tag.children
        if isinstance(child, NavigableString)
    ).strip()


def _fetch(url, params, headers, use_ssl_adapter=False, timeout=15):
    """HTTP GET 요청을 수행합니다."""
    if use_ssl_adapter:
        session = requests.Session()
        session.mount('https://', _SslAdapter())
        try:
            resp = session.get(url, params=params, headers=headers, timeout=timeout, verify=False)
            return resp
        finally:
            session.close()
    else:
        return requests.get(url, params=params, headers=headers, timeout=timeout)


class JnetTypeAScraper(LibraryScraper):
    """
    jnet Type A 스크래퍼 (searchResultList.do)
    구리/과천/고양/양평 등과 동일한 패턴.
    - 총 건수: #totalCnt
    - 도서 목록: #bookList > div > ul > li
    - html5lib 파서 사용
    """

    def __init__(self, region_name: str, domain: str, site_code: str = "intro",
                 menu_id: str = "10003", program_id: str = "30001",
                 use_ssl_adapter: bool = False):
        self._domain = domain
        self._site_code = site_code
        self._use_ssl_adapter = use_ssl_adapter
        base_url = f"https://{domain}/{site_code}/menu/{menu_id}/program/{program_id}/searchResultList.do"
        super().__init__(region_name=region_name, base_url=base_url)

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        if author:
            params = {
                "searchType": "DETAIL",
                "searchAdvTitle": title,
                "searchAdvAuthor": author,
                "searchArticle": "SCORE",
                "searchOrder": "ASC",
                "searchManageCode": "ALL",
                "searchDisplay": "100",
            }
        else:
            params = {
                "searchType": "SIMPLE",
                "searchKeyword": title,
                "searchArticle": "SCORE",
                "searchOrder": "ASC",
                "searchManageCode": "ALL",
                "searchDisplay": "100",
            }

        all_books = []
        total_count = 0
        page = 1

        while True:
            params["currentPageNo"] = str(page)

            try:
                resp = _fetch(self.base_url, params, self._headers, self._use_ssl_adapter)
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"  [오류] {self.region_name} 도서관 접속 실패: {e}")
                return total_count, all_books

            soup = BeautifulSoup(resp.text, "html5lib")

            # 첫 페이지에서 총 검색 건수 파싱
            if page == 1:
                total_cnt_tag = soup.select_one("#totalCnt")
                if not total_cnt_tag:
                    total_cnt_tag = soup.select_one(
                        "#searchForm > div:nth-of-type(2) > div > div:nth-of-type(1) > div > span"
                    )
                total_count = _parse_int(total_cnt_tag.text) if total_cnt_tag else 0
                if total_count == 0:
                    return 0, []

            # 도서 목록 파싱
            book_items = soup.select("#bookList li")
            if not book_items:
                book_items = soup.select(".bookArea")

            if not book_items:
                break

            for item in book_items:
                area = item.select_one(".bookArea") or item
                book = BookInfo(region=self.region_name)

                # 1. 제목: a.book_name
                title_tag = area.select_one("a.book_name")
                if title_tag:
                    # span.kor.on 내 텍스트 우선 추출
                    kor_span = title_tag.select_one("span.kor.on")
                    if kor_span:
                        book.title = kor_span.text.strip()
                    else:
                        book.title = title_tag.text.strip()
                
                # 2. 저자: info01의 첫 번째 p 태그
                info01 = area.select_one(".info01 .kor.on") or area.select_one(".info01")
                if info01:
                    p_tags = info01.select("p")
                    if p_tags:
                        book.author = p_tags[0].text.strip()

                # 3. 청구기호: info02 내의 p 태그 중 텍스트 추출 (버튼 텍스트 제외)
                info02 = area.select_one(".info02")
                if info02:
                    p_tag = info02.select_one("p")
                    if p_tag:
                        direct_val = _direct_text(p_tag)
                        if not direct_val and p_tag.contents:
                            # 첫번째 자식 노드가 텍스트일 때
                            first = p_tag.contents[0]
                            if isinstance(first, NavigableString):
                                direct_val = first.strip()
                        book.call_number = direct_val or p_tag.text.replace("청구기호", "").replace("청구", "").replace("인쇄", "").strip()

                # 4. 소장 도서관 및 자료실: info03
                info03 = area.select_one(".info03")
                if info03:
                    p_tag = info03.select_one("p")
                    if p_tag:
                        book.location = p_tag.text.strip()
                        match = re.search(r'\[(.+?)\]', book.location)
                        if match:
                            lib_base = match.group(1).strip()
                            book.library = lib_base if lib_base.endswith("도서관") else lib_base + "도서관"
                        else:
                            book.library = book.location

                if not book.library:
                    book.library = f"{self.region_name}도서관"
                
                # 강남구립도서관도서관 같은 중복명 수정
                if "도서관도서관" in book.library:
                    book.library = book.library.replace("도서관도서관", "도서관")

                if book.title:
                    all_books.append(book)

            if len(all_books) >= total_count:
                break
            page += 1

        return total_count, all_books


class JnetTypeBScraper(LibraryScraper):
    """
    jnet Type B 스크래퍼 (plusSearchResultList.do)
    용인/성남/남양주/평택/포천/강남구립 등과 동일한 패턴.
    - 도서 목록: ul.resultList > li
    - 각 도서: dl.bookDataWrap 내 dt.tit, dd.author, dd.data, dd.site
    """

    def __init__(self, region_name: str, domain: str, site_code: str = "intro",
                 menu_id: str = "10181", program_id: str = "30012",
                 use_ssl_adapter: bool = False):
        self._domain = domain
        self._site_code = site_code
        self._use_ssl_adapter = use_ssl_adapter
        base_url = f"https://{domain}/{site_code}/menu/{menu_id}/program/{program_id}/plusSearchResultList.do"
        super().__init__(region_name=region_name, base_url=base_url)

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        if author:
            params = {
                "searchType": "DETAIL",
                "searchCategory": "BOOK",
                "searchKey1": "TITLE",
                "searchKeyword1": title,
                "searchOperator1": "AND",
                "searchKey2": "AUTHOR",
                "searchKeyword2": author,
                "searchOperator2": "AND",
                "searchOrder": "DESC",
                "searchManageCode": "ALL",
                "searchDisplay": "100",
            }
        else:
            params = {
                "searchType": "SIMPLE",
                "searchCategory": "BOOK",
                "searchKey": "ALL",
                "searchKeyword": title,
                "searchOrder": "DESC",
                "searchManageCode": "ALL",
                "searchDisplay": "100",
            }

        all_books = []
        total_count = 0
        page = 1

        while True:
            params["currentPageNo"] = str(page)

            try:
                resp = _fetch(self.base_url, params, self._headers, self._use_ssl_adapter)
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"  [오류] {self.region_name} 도서관 접속 실패: {e}")
                return total_count, all_books

            soup = BeautifulSoup(resp.text, "html.parser")

            if page == 1:
                cnt_tag = soup.select_one("#totalCnt") or soup.select_one(".totalCnt") or soup.select_one(".total > span")
                total_count = _parse_int(cnt_tag.text) if cnt_tag else 0

            # 도서 목록: ul.resultList > li 또는 .bookArea
            book_items = soup.select("ul.resultList > li") or soup.select(".bookArea")
            if not book_items:
                break

            if total_count == 0:
                total_count = len(book_items)

            for item in book_items:
                book = BookInfo(region=self.region_name)

                # bookArea 형태인 경우 (오산/용인 등)
                classes = item.get("class", [])
                if classes and "bookArea" in classes:
                    title_tag = item.select_one(".book_name a, a.book_name, .book_name")
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
                else:
                    dl = item.select_one("dl.bookDataWrap")
                    if not dl:
                        continue

                    # 제목: dt.tit > a
                    title_tag = dl.select_one("dt.tit > a")
                    if title_tag:
                        raw_title = title_tag.text.strip()
                        raw_title = re.sub(r'^\d+\.\s*', '', raw_title)
                        book.title = raw_title

                    # 저자 및 청구기호 추출
                    all_spans = dl.select("dd span")
                    for sp in all_spans:
                        direct = _direct_text(sp)
                        full_txt = sp.text.strip()
                        
                        # 1. 저자
                        if ("저자" in full_txt or "저 :" in full_txt or "저자:" in full_txt) and not book.author:
                            raw_author = re.sub(r'^저자?\s*:\s*', '', full_txt).strip()
                            book.author = raw_author
                        
                        # 2. 청구기호
                        if "청구기호" in direct or "청구번호" in direct or "청구" in direct:
                            call_match = re.search(r'(?:청구기호|청구번호|청구)\s*:\s*(.+)', direct)
                            if call_match:
                                book.call_number = call_match.group(1).strip()
                        txt = sp.text.strip()
                        if "소장" in txt and ":" in txt:
                            lib_name = re.sub(r'^소장\s*:\s*', '', txt).strip()
                            book.library = lib_name
                        elif "자료실" in txt and ":" in txt:
                            loc = re.sub(r'^자료실\s*:\s*', '', txt).strip()
                            book.location = loc

                if not book.library:
                    book.library = f"{self.region_name}도서관"
                
                # 중복 명칭 제거
                if "도서관도서관" in book.library:
                    book.library = book.library.replace("도서관도서관", "도서관")

                if book.title:
                    all_books.append(book)

            if len(all_books) >= total_count:
                break
            page += 1

        return total_count, all_books
