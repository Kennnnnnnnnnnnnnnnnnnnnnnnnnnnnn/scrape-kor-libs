"""
경기도 31개 시/군 공공도서관 스크래퍼 모듈
- jnet 엔드포인트가 확인된 도서관: 실제 스크래퍼 등록
- 수원시 도서관: 모바일 API 기반 전용 스크래퍼 등록 (POST 방식 고정)
- 안산시 도서관: Vue API 기반 전용 스크래퍼 등록 (POST JSON 방식)
- 미확인 도서관: GenericLibraryScraper (빈 결과 반환)
"""
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

from .registry import register_scraper
from .jnet import JnetTypeAScraper, JnetTypeBScraper, _SslAdapter
from .generic import GenericLibraryScraper
from .base import LibraryScraper, BookInfo
from typing import List, Tuple, Dict
from bs4 import BeautifulSoup


# ========================================================================
# 수원시 도서관 - 모바일 API 기반 전용 스크래퍼
# ========================================================================

class SuwonScraper(LibraryScraper):
    """수원시 도서관 실시간 검색 스크래퍼 (모바일 API 연동 - POST 방식)"""

    def __init__(self):
        super().__init__(
            region_name="수원시",
            base_url="https://mob.suwonlib.go.kr/getSearchResult/BOOK"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = self._headers.copy()
        headers["ajax"] = "true"
        headers["X-Requested-With"] = "XMLHttpRequest"

        all_books = []
        total_count = 0
        page = 1

        while True:
            payload = {
                "searchTxt": query,
                "searchKind": "SIMPLE",
                "manageCode": "",
                "isInnerSearch": "F",
                "innerSearchTxt": "",
                "keywordSearch": "false",
                "displayNo": "100",
                "orderbyItem": "SCORE",
                "orderby": "ASC",
                "pageNo": str(page),
                "kCid": "",
                "kdcValue": ""
            }

            try:
                session = requests.Session()
                session.mount('https://', _SslAdapter())
                resp = session.post(self.base_url, data=payload, headers=headers, timeout=15, verify=False)
                resp.raise_for_status()
                data = resp.json()
                session.close()
            except Exception as e:
                print(f"  [오류] 수원시 도서관 접속 실패: {e}")
                return total_count, all_books

            res = data.get("SEARCH_RESULT", {})
            if page == 1:
                total_count = res.get("SEARCH_COUNT", 0)

            book_list = res.get("SEARCH_LIST", [])
            if not book_list:
                break

            for bdata in book_list:
                book = BookInfo(region="경기도")

                raw_title = bdata.get("TITLE_INFO", "")
                cleaned_title = re.sub(r'<.*?>', '', raw_title).strip()
                book.title = cleaned_title

                book.author = bdata.get("AUTHOR", "").strip()
                book.publisher = bdata.get("PUBLISHER", "").strip()
                book.call_number = bdata.get("CALL_NO", "").strip()
                
                lib_name = bdata.get("LIB_NAME", "").strip()
                book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                book.location = bdata.get("SHELF_LOC_NAME", "").strip()

                if "도서관도서관" in book.library:
                    book.library = book.library.replace("도서관도서관", "도서관")

                if book.title:
                    all_books.append(book)

            if len(all_books) >= total_count or len(book_list) == 0:
                break
            page += 1

        return total_count, all_books

register_scraper("수원시", SuwonScraper, metro_name="경기도")


# ========================================================================
# 안산시 도서관 - Vue API 기반 전용 스크래퍼
# ========================================================================

class AnsanScraper(LibraryScraper):
    """안산시 도서관 실시간 검색 스크래퍼 (Vue API 연동 - POST JSON 방식)"""

    def __init__(self):
        super().__init__(
            region_name="안산시",
            base_url="http://lib.iansan.net/api/search"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        all_books = []
        total_count = 0
        page = 1

        while True:
            payload = {
                "searchKeyword": query,
                "page": str(page),
                "display": "100"
            }

            try:
                resp = requests.post(self.base_url, json=payload, headers=self._headers, timeout=15)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"  [오류] 안산시 도서관 접속 실패: {e}")
                return total_count, all_books

            contents = data.get("contents", {})
            if page == 1:
                total_count = contents.get("totalCount", 0)

            book_list = contents.get("bookList", []) or contents.get("list", [])
            if not book_list:
                break

            for bdata in book_list:
                book = BookInfo(region="경기도")

                raw_title = bdata.get("title", "")
                cleaned_title = re.sub(r'<.*?>', '', raw_title).strip()
                book.title = cleaned_title

                book.author = bdata.get("author", "").strip()
                book.publisher = bdata.get("publisher", "").strip()
                book.call_number = bdata.get("callNo", "").strip()
                
                lib_name = bdata.get("libName", "").strip()
                book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                book.location = bdata.get("shelfLocName", "").strip()

                if "도서관도서관" in book.library:
                    book.library = book.library.replace("도서관도서관", "도서관")

                if book.title:
                    all_books.append(book)

            if len(all_books) >= total_count or len(book_list) == 0:
                break
            page += 1

        return total_count, all_books

register_scraper("안산시", AnsanScraper, metro_name="경기도")


# ========================================================================
# jnet Type A (searchResultList.do) 확인된 사이트
# ========================================================================

# 구리시
class GuriScraper(JnetTypeAScraper):
    def __init__(self):
        super().__init__(region_name="구리시", domain="www.gurilib.go.kr", use_ssl_adapter=True)

register_scraper("구리시", GuriScraper, metro_name="경기도")


# 과천시
class GwacheonScraper(JnetTypeAScraper):
    def __init__(self):
        super().__init__(region_name="과천시", domain="www.gclib.go.kr")

register_scraper("과천시", GwacheonScraper, metro_name="경기도")


# 고양시
class GoyangScraper(JnetTypeAScraper):
    def __init__(self):
        super().__init__(region_name="고양시", domain="www.goyanglib.or.kr")

register_scraper("고양시", GoyangScraper, metro_name="경기도")


# 양평군
class YangpyeongScraper(LibraryScraper):
    """양평군 통합도서관 스크래퍼 (www.yplib.go.kr - AlpasQ API 연동)"""
    def __init__(self):
        super().__init__(
            region_name="양평군",
            base_url="https://www.yplib.go.kr/api/search"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchKeyword": query,
            "page": 1,
            "display": 100,
            "manageCode": "ALL"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.yplib.go.kr/'
        }

        try:
            r = self._session.post(self.base_url, json=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"  [오류] 양평군 도서관 검색 실패: {e}")
            return 0, []

        contents = data.get("contents", {})
        total_count = contents.get("totalCount", 0)
        items = contents.get("bookList", [])

        books = []
        for item in items:
            book_title = item.get("originalTitle") or item.get("title", "")
            book_title = re.sub(r"<[^>]+>", "", book_title).strip()
            
            book_author = item.get("originalAuthor") or item.get("author", "")
            book_author = re.sub(r"\s*저\.?|\s*지음", "", book_author).strip()

            lib_name = item.get("libName", "양평군도서관")
            if not lib_name.endswith("도서관"):
                lib_name += "도서관"

            call_no = item.get("callNo", "").strip()
            location = item.get("shelfLocName", "").strip()

            if lib_name:
                book = BookInfo(region="경기도")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                book.location = location
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("양평군", YangpyeongScraper, metro_name="경기도")


# ========================================================================
# jnet Type B (plusSearchResultList.do) 확인된 사이트
# ========================================================================

# 성남시
class SeongnamScraper(JnetTypeBScraper):
    def __init__(self):
        super().__init__(region_name="성남시", domain="www.snlib.go.kr")

register_scraper("성남시", SeongnamScraper, metro_name="경기도")


# 남양주시
class NamyangjuScraper(JnetTypeBScraper):
    def __init__(self):
        super().__init__(region_name="남양주시", domain="lib.nyj.go.kr", use_ssl_adapter=True)

register_scraper("남양주시", NamyangjuScraper, metro_name="경기도")


# 평택시
class PyeongtaekScraper(JnetTypeBScraper):
    def __init__(self):
        super().__init__(region_name="평택시", domain="www.ptlib.go.kr")

register_scraper("평택시", PyeongtaekScraper, metro_name="경기도")


# 오산시
class OsanScraper(JnetTypeBScraper):
    def __init__(self):
        super().__init__(region_name="오산시", domain="www.osanlibrary.go.kr", use_ssl_adapter=True)

register_scraper("오산시", OsanScraper, metro_name="경기도")


# 포천시
class PocheonScraper(JnetTypeBScraper):
    def __init__(self):
        super().__init__(region_name="포천시", domain="lib.pocheon.go.kr")

register_scraper("포천시", PocheonScraper, metro_name="경기도")


# ========================================================================
# 광명시 도서관 - DLS 솔루션 기반 전용 스크래퍼
# ========================================================================

class GwangmyeongScraper(LibraryScraper):
    """광명시 도서관 실시간 검색 스크래퍼 (DLS 솔루션 기반 - 1차 검색 후 2차 상세페이지 소장정보 연동)"""

    def __init__(self):
        super().__init__(
            region_name="광명시",
            base_url="https://gmlib.gm.go.kr/dls_le/index.php"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "mod": "wdDataSearch",
            "act": "searchIList",
            "item": "total",
            "word": query
        }

        try:
            resp = requests.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 광명시 도서관 1차 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")

        # 1차 목록 수집 (체크박스가 들어있는 진짜 도서 카드만 수집)
        items = []
        for div in soup.select("div.list"):
            if div.select_one("input.listCheck") or div.select_one(".listCheck"):
                items.append(div)
                
        total_count = len(items)

        if not items:
            return 0, []

        books = []
        # 트래픽 절약을 위해 상위 7건에 대해서만 2차 상세 소장정보 요청
        for item in items[:7]:
            # 1. 1차 정보 파싱
            # 제목: 체크박스의 title 속성에서 순수 제목을 깔끔하게 추출 (html 깨짐 방지)
            chk = item.select_one("input.listCheck")
            if chk:
                base_title = chk.get("title", "").replace(" 선택", "").replace("선택", "").strip()
            else:
                title_tag = item.select_one("div.ico a")
                base_title = title_tag.text.strip() if title_tag else "광명도서"

            # 저자
            base_author = ""
            li_tags = item.select("dd ul li")
            for li in li_tags:
                txt = li.text.strip()
                if "저자" in txt or "저 " in txt or "ㆍ저" in txt:
                    base_author = txt.replace("저자", "").replace("ㆍ", "").replace(":", "").replace("|", "").strip()
                    break

            # 2. XHR 상세페이지 파라미터 추출
            detail_link = None
            for a_tag in item.select("a"):
                href = a_tag.get("href", "")
                if "searchResultDetail" in href:
                    detail_link = a_tag
                    break

            if not detail_link:
                continue

            href = detail_link.get("href", "")
            m_jong = re.search(r"jongKey=([^&]+)", href)
            m_book = re.search(r"bookKey=([^&]+)", href)
            if not m_jong or not m_book:
                continue

            jong_key = m_jong.group(1).strip()
            book_key = m_book.group(1).strip()

            # 3. 2차 상세페이지 호출
            detail_params = {
                "mod": "wdDataSearch",
                "act": "searchResultDetail",
                "dbType": "dan",
                "jongKey": jong_key,
                "bookKey": book_key
            }

            try:
                d_resp = requests.get(self.base_url, params=detail_params, headers=self._headers, timeout=8, verify=False)
                if d_resp.status_code == 200:
                    dsoup = BeautifulSoup(d_resp.text, "html.parser")
                    rows = dsoup.select("table tbody tr")
                    for row in rows:
                        tds = row.select("td")
                        if len(tds) >= 4:
                            # 불필요한 서브밋/프린트 버튼 텍스트 전처리 제거
                            raw_call = tds[2].text.replace("청구기호", "").replace("인쇄", "").replace("출력", "").strip()
                            
                            # 모든 줄바꿈 및 탭을 공백(" ")으로 치환하여 단어 붙는 버그 차단
                            clean_call = raw_call.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()
                            # 다중 공백을 단일 공백으로 치환
                            clean_call = re.sub(r"\s+", " ", clean_call)
                            
                            # 대괄호 위치 찾기
                            if clean_call.startswith("[") and "]" in clean_call:
                                idx_end = clean_call.find("]")
                                lib_loc = clean_call[1:idx_end].strip() # 하안
                                book_loc = clean_call[idx_end+1:].strip() # 자료실 005.133-이655파
                                
                                # 공백 분리 알고리즘으로 청구기호와 자료실 위치 정교하게 쪼개기
                                parts = book_loc.split()
                                if len(parts) >= 2:
                                    if len(parts) >= 3 and len(parts[-2]) == 1:
                                        call_no = parts[-2] + " " + parts[-1]
                                        shelf_loc = " ".join(parts[:-2])
                                    else:
                                        call_no = parts[-1]
                                        shelf_loc = " ".join(parts[:-1])
                                else:
                                    call_no = book_loc
                                    shelf_loc = ""
                                
                                # 2번째 td인 도서관명이 우선, 없으면 lib_loc 접두사 활용
                                lib_name_col = tds[1].text.strip()
                                if lib_name_col and lib_name_col != "-":
                                    lib_name = lib_name_col
                                else:
                                    lib_name = lib_loc + "도서관" if not lib_loc.endswith("도서관") else lib_loc
                            else:
                                call_no = clean_call
                                shelf_loc = ""
                                lib_name = tds[1].text.strip() if (len(tds) > 1 and tds[1].text.strip() != "-") else "광명시도서관"

                            book = BookInfo(region="경기도")
                            book.title = base_title
                            book.author = base_author
                            book.library = lib_name
                            book.call_number = call_no
                            book.location = shelf_loc

                            if "도서관도서관" in book.library:
                                book.library = book.library.replace("도서관도서관", "도서관")

                            books.append(book)
            except Exception:
                pass

        return total_count, books

register_scraper("광명시", GwangmyeongScraper, metro_name="경기도")
register_scraper("광명시립도서관", GwangmyeongScraper, metro_name="경기도")


# ========================================================================
# 의정부시 도서관 - JNET 커스텀 기반 전용 스크래퍼
# ========================================================================

class UijeongbuScraper(LibraryScraper):
    """의정부시 도서관 실시간 검색 스크래퍼 (HTTPS SSL 암호화수준 강하 및 bookkey 연동)"""

    def __init__(self):
        super().__init__(
            region_name="의정부시",
            base_url="https://www.uilib.go.kr/main/intro/search/index.do"
        )
        # 구버전 SSL 암호화 수준 보안 강하 전용 어댑터 설정
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menu_idx": "9",
            "booktype": "ALL",
            "title": query
        }

        try:
            resp = self._session.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 의정부시 도서관 1차 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(".item")
        
        # 총 검색 건수 파싱 (결과 수 카운트가 별도로 없을 시 목록 개수 기준)
        total_count = len(items)
        if not items:
            return 0, []

        books = []
        # 트래픽 절약 및 속도를 위해 상위 7건에 대해서만 2차 상세 소장정보 요청
        for item in items[:7]:
            # 1. 1차 정보 파싱
            title_tag = item.select_one("a.name")
            if not title_tag:
                continue
            base_title = title_tag.text.strip()
            
            # 저자
            base_author = ""
            p_tags = item.select(".contents p")
            for p in p_tags:
                p_txt = p.text.strip()
                if "저자" in p_txt or "ڻ" in p_txt:  # 인코딩 깨짐 대응용
                    base_author = p_txt.replace("저자", "").replace(":", "").strip()
                    break

            # 상세 링크에서 bookkey, speciesKey, isbn, booktype 추출
            href = title_tag.get("href", "")
            m_isbn = re.search(r"isbn=([^&]+)", href)
            m_sp = re.search(r"speciesKey=([^&]+)", href)
            m_bk = re.search(r"bookkey=([^&]+)", href)
            m_bt = re.search(r"booktype=([^&]+)", href)

            if not m_isbn or not m_sp or not m_bk:
                continue

            isbn = m_isbn.group(1).strip()
            species_key = m_sp.group(1).strip()
            book_key = m_bk.group(1).strip()
            booktype = m_bt.group(1).strip() if m_bt else "MO"

            # 2. 2차 상세페이지 소장정보 호출
            detail_url = "https://www.uilib.go.kr/main/intro/search/detail.do"
            d_params = {
                "menu_idx": "9",
                "isbn": isbn,
                "speciesKey": species_key,
                "bookkey": book_key,
                "booktype": booktype
            }

            try:
                d_resp = self._session.get(detail_url, params=d_params, headers=self._headers, timeout=8, verify=False)
                if d_resp.status_code == 200:
                    dsoup = BeautifulSoup(d_resp.text, "html.parser")
                    tables = dsoup.select("table")
                    for table in tables:
                        headers = [th.text.strip() for th in table.select("th")]
                        # 도서관 및 청구기호 컬럼이 존재하는 소장 테이블만 탐색
                        if any(h in "".join(headers) for h in ["도서관", "청구기호", "û"]):
                            rows = table.select("tbody tr")
                            for row in rows:
                                tds = row.select("td")
                                if len(tds) >= 3:
                                    lib_name = tds[0].text.strip()
                                    loc_name = tds[1].text.strip()
                                    call_no = tds[2].text.strip()
                                    
                                    # 유효한 도서관 데이터인 경우에만 수집 (빈 껍데기 줄 제외)
                                    if lib_name and call_no:
                                        book = BookInfo(region="경기도")
                                        book.title = base_title
                                        book.author = base_author
                                        book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                                        book.call_number = call_no
                                        book.location = loc_name
                                        
                                        books.append(book)
            except Exception:
                pass

        return total_count, books

register_scraper("의정부시", UijeongbuScraper, metro_name="경기도")
register_scraper("의정부시립도서관", UijeongbuScraper, metro_name="경기도")


# ========================================================================
# 김포시 도서관 - 자체 포털 기반 전용 스크래퍼 (1차 검색 결과 data- 속성 활용)
# ========================================================================

class GimpoScraper(LibraryScraper):
    """김포시 도서관 실시간 검색 스크래퍼 (1차 검색 응답 데이터 내 data-callno 속성 활용 기법)"""

    def __init__(self):
        super().__init__(
            region_name="김포시",
            base_url="https://www.gimpo.go.kr/modam/bookSearchList.do?allCheck=ALL"
        )
        # 구버전 SSL 암호화 수준 보안 강하 전용 어댑터 설정
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "rep": "1",
            "key": "11488",
            "manageCode": "BR,DK,GC,GR,HS,JG,MA,MS,PM,TJ,YG,YY,MD",
            "searchKrwd": query
        }

        try:
            resp = self._session.post(self.base_url, data=payload, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 김포시 도서관 통합검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # data-callno 속성을 품고 있는 a 태그 수집
        tags = soup.select("[data-callno]")
        total_count = len(tags)
        
        if not tags:
            return 0, []

        books = []
        for tag in tags:
            lib_name = tag.get("data-libname", "").strip()
            call_no = tag.get("data-callno", "").strip()
            raw_title = tag.get("data-titleinfo", "").strip()
            
            # 저자 정보는 상위 parent 구조를 따라가며 추출
            base_author = ""
            parent_item = tag.find_parent("div", class_="item") or tag.find_parent("div")
            if parent_item:
                li_tags = parent_item.select("ul.clearfix li")
                for li in li_tags:
                    txt = li.text.strip()
                    if "저자" in txt or "저 " in txt or "지음" in txt:
                        base_author = txt.replace("저자", "").replace("지음", "").replace(":", "").replace("|", "").strip()
                        break

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = raw_title
                book.author = base_author
                book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                book.call_number = call_no
                book.location = ""
                
                books.append(book)

        return total_count, books

register_scraper("김포시", GimpoScraper, metro_name="경기도")
register_scraper("김포시립도서관", GimpoScraper, metro_name="경기도")


# ========================================================================
# 파주시 도서관 - 포털 기반 전용 스크래퍼
# ========================================================================

class PajuScraper(LibraryScraper):
    """파주시 도서관 실시간 검색 스크래퍼 (csSignature 사전 획득 및 1차 목록 파싱 기법)"""

    def __init__(self):
        super().__init__(
            region_name="파주시",
            base_url="https://lib.paju.go.kr/jalib/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        
        # 1. csSignature 획득을 위해 메인 인덱스 접속
        try:
            r_main = self._session.get("https://lib.paju.go.kr/intro/index.do", headers=self._headers, timeout=10, verify=False)
            soup_main = BeautifulSoup(r_main.text, "html.parser")
            sig_tag = soup_main.select_one("form#topSearchForm input[name='csSignature']")
            sig = sig_tag.get("value") if sig_tag else "SA36ZE/FvK91IHCpSe0kEQ=="
        except Exception:
            sig = "SA36ZE/FvK91IHCpSe0kEQ=="

        # 2. 통합 검색 요청
        params = {
            "csSignature": sig,
            "searchType": "SIMPLE",
            "searchCategory": "ALL",
            "searchLibrary": "ALL",
            "searchKey": "ALL",
            "searchKeyword": query
        }

        try:
            resp = self._session.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 파주시 도서관 통합검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 전체 검색 건수 파싱
        total_count = 0
        cnt_tag = soup.select_one("strong.searchKwd ~ b.themeFC")
        if cnt_tag:
            try:
                total_count = int(re.sub(r"[^\d]", "", cnt_tag.text))
            except ValueError:
                pass

        # 도서 목록 탐색
        book_items = soup.select("dl.bookDataWrap")
        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            # 제목
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            raw_title = title_tag.text.strip()
            # "1. ", "2. " 등 접두 숫자 제거
            raw_title = re.sub(r"^\d+\.\s*", "", raw_title)

            # 저자
            base_author = ""
            author_tag = item.select_one("dd.author span")
            if author_tag:
                base_author = author_tag.text.strip()
                # "저 : ", "저자 : " 제거
                base_author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", base_author)

            # 청구기호
            call_no = ""
            data_spans = item.select("dd.data span")
            for span in data_spans:
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").replace("위치", "").strip()
                    # 잔여 줄바꿈 및 탭 클렌징
                    call_no = re.sub(r"\s+", " ", call_no).strip()
                    break

            # 도서관명
            lib_name = ""
            site_spans = item.select("dd.site span")
            for span in site_spans:
                txt = span.text.strip()
                if "관:" in txt or "도서관" in txt or "관 " in txt:
                    lib_name = txt.replace("관", "").replace(":", "").strip()
                    lib_name = re.sub(r"\s+", " ", lib_name).strip()
                    break

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = raw_title
                book.author = base_author
                book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                book.call_number = call_no
                book.location = ""
                
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("파주시", PajuScraper, metro_name="경기도")
register_scraper("파주시립도서관", PajuScraper, metro_name="경기도")


# ========================================================================
# 하남시 도서관 - 포털 iframe 기반 전용 스크래퍼
# ========================================================================

class HanamScraper(LibraryScraper):
    """하남시 도서관 실시간 검색 스크래퍼 (다중 지점코드 동시 조립 및 1차 검색결과 수집 기법)"""

    def __init__(self):
        super().__init__(
            region_name="하남시",
            base_url="https://www.hanamlib.go.kr/kolaseek/search/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        
        # 하남시 관내 주요 지점 코드 목록 전수 빌딩
        libs_arr = ["MB", "MS", "WI", "SJ", "GL", "SE", "DI", "DP", "IG"]
        
        # 다중 searchLibraryArr 매개변수 구조 빌드
        params = []
        for code in libs_arr:
            params.append(("searchLibraryArr", code))
        
        params.extend([
            ("searchKeyword", query),
            ("searchType", "SIMPLE"),
            ("searchCategory", "ALL"),
            ("searchKey", "ALL")
        ])

        try:
            resp = self._session.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 하남시 도서관 통합검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 전체 검색 건수 파싱
        total_count = 0
        cnt_tag = soup.select_one("strong.searcKwd ~ span.themeFC, strong.searcKwd ~ b.themeFC")
        if not cnt_tag:
            cnt_tag = soup.select_one("span.themeFC")
        if cnt_tag:
            try:
                total_count = int(re.sub(r"[^\d]", "", cnt_tag.text))
            except ValueError:
                pass

        book_items = soup.select("dl.bookDataWrap")
        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            # 제목
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            raw_title = title_tag.text.strip()
            # 접두 숫자 제거 (예: "1. 파이썬" -> "파이썬")
            raw_title = re.sub(r"^\d+\.\s*", "", raw_title)

            # 저자
            base_author = ""
            author_tag = item.select_one("dd.author span")
            if author_tag:
                base_author = author_tag.text.strip()
                # "저자 : ", "저 : " 제거
                base_author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", base_author)

            # 청구기호
            call_no = ""
            data_spans = item.select("dd.data span")
            for span in data_spans:
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").replace("위치", "").strip()
                    call_no = re.sub(r"\s+", " ", call_no).strip()
                    break

            # 도서관명
            lib_name = ""
            site_spans = item.select("dd.site span")
            for span in site_spans:
                txt = span.text.strip()
                if "관:" in txt or "도서관" in txt or "관 " in txt:
                    lib_name = txt.replace("관", "").replace(":", "").strip()
                    lib_name = re.sub(r"\s+", " ", lib_name).strip()
                    break

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = raw_title
                book.author = base_author
                book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                book.call_number = call_no
                book.location = ""
                
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("하남시", HanamScraper, metro_name="경기도")
register_scraper("하남시립도서관", HanamScraper, metro_name="경기도")


# ========================================================================
# 이천시 도서관 - 포털 기반 전용 스크래퍼
# ========================================================================

class IcheonScraper(LibraryScraper):
    """이천시 도서관 실시간 검색 스크래퍼 (1차 검색 후 2차 상세페이지 소장정보 연동 기법)"""

    def __init__(self):
        super().__init__(
            region_name="이천시",
            base_url="https://www.icheonlib.go.kr/search/tot/result"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "si": "TOTAL",
            "st": "KWRD",
            "q": query
        }

        try:
            resp = self._session.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 이천시 도서관 1차 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 도서 링크들 탐색 (a[href*='/search/detail/'])
        detail_links = soup.select("dd.book a[href*='/search/detail/'], a[href*='/search/detail/']")
        if not detail_links:
            return 0, []

        books = []
        total_count = len(detail_links)
        
        # 트래픽 및 속도를 위해 상위 8건에 대해서만 2차 상세 소장정보 요청
        seen_urls = set()
        for link in detail_links:
            href = link.get("href", "")
            if not href or href in seen_urls:
                continue
            seen_urls.add(href)
            
            # 절대 경로 빌드
            if href.startswith("/"):
                detail_url = "https://www.icheonlib.go.kr" + href
            else:
                detail_url = href

            # 1차 제목 추출
            base_title = link.text.strip()
            # 접두 숫자 제거 (예: "1. 파이썬" -> "파이썬")
            base_title = re.sub(r"^\d+\.\s*", "", base_title)

            # 저자는 부모의 dd span 등에서 탐색
            base_author = ""
            parent_dd = link.find_parent("dd")
            if parent_dd:
                author_span = parent_dd.select_one("span")
                if author_span:
                    base_author = author_span.text.strip().split("|")[0].strip()

            if len(seen_urls) > 8:
                break

            # 2차 상세페이지 호출
            try:
                d_resp = self._session.get(detail_url, headers=self._headers, timeout=8, verify=False)
                if d_resp.status_code == 200:
                    dsoup = BeautifulSoup(d_resp.text, "html.parser")
                    tables = dsoup.select("table")
                    for table in tables:
                        headers = [th.text.strip() for th in table.select("th")]
                        if any(h in "".join(headers) for h in ["청구기호", "소장처", "도서상태"]):
                            rows = table.select("tbody tr")
                            for row in rows:
                                tds = row.select("td")
                                if len(tds) >= 5:
                                    # JNET 표준 셀 인덱스
                                    # No | 등록번호 | 청구기호 | 소장처/자료실 | 도서상태 | 반납예정일 ...
                                    call_no = tds[2].text.strip()
                                    lib_loc = tds[3].text.strip()
                                    
                                    # 소장처 가공 (예: "시립도서관어린이실/어린이/" -> "시립도서관")
                                    lib_name = lib_loc.split("/")[0].strip() if "/" in lib_loc else lib_loc
                                    loc_name = lib_loc.split("/")[1].strip() if "/" in lib_loc and len(lib_loc.split("/")) > 1 else ""
                                    
                                    if lib_name and call_no:
                                        book = BookInfo(region="경기도")
                                        book.title = base_title
                                        book.author = base_author
                                        book.library = lib_name if lib_name.endswith("도서관") or lib_name.endswith("실") else lib_name + "도서관"
                                        book.call_number = call_no
                                        book.location = loc_name
                                        
                                        books.append(book)
            except Exception:
                pass

        return total_count, books

register_scraper("이천시", IcheonScraper, metro_name="경기도")
register_scraper("이천시립도서관", IcheonScraper, metro_name="경기도")


# ========================================================================
# 양주시 도서관 - ojlake 기반 전용 스크래퍼
# ========================================================================

class YangjuScraper(LibraryScraper):
    """양주시 도서관 실시간 검색 스크래퍼 (ojlake 포털 기반 단일 GET 통신 및 1차 검색결과 수집 기법)"""

    def __init__(self):
        super().__init__(
            region_name="양주시",
            base_url="https://www.libyj.go.kr/ojlake/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "searchKeyword": query,
            "searchType": "SIMPLE",
            "searchCategory": "ALL",
            "searchKey": "ALL"
        }

        try:
            resp = self._session.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 양주시 도서관 통합검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 전체 검색 건수 파싱
        total_count = 0
        cnt_tag = soup.select_one("strong.searcKwd ~ span.themeFC, strong.searcKwd ~ b.themeFC")
        if not cnt_tag:
            cnt_tag = soup.select_one("span.themeFC")
        if cnt_tag:
            try:
                total_count = int(re.sub(r"[^\d]", "", cnt_tag.text))
            except ValueError:
                pass

        book_items = soup.select("dl.bookDataWrap")
        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            # 제목
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            raw_title = title_tag.text.strip()
            # 접두 숫자 제거 (예: "1. 파이썬" -> "파이썬")
            raw_title = re.sub(r"^\d+\.\s*", "", raw_title)

            # 저자
            base_author = ""
            author_tag = item.select_one("dd.author span")
            if author_tag:
                base_author = author_tag.text.strip()
                # "저자 : ", "저 : " 제거
                base_author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", base_author)

            # 청구기호
            call_no = ""
            data_spans = item.select("dd.data span")
            for span in data_spans:
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").replace("위치", "").strip()
                    call_no = re.sub(r"\s+", " ", call_no).strip()
                    break

            # 도서관명
            lib_name = ""
            site_spans = item.select("dd.site span")
            for span in site_spans:
                txt = span.text.strip()
                if "관:" in txt or "도서관" in txt or "관 " in txt:
                    lib_name = txt.replace("관", "").replace(":", "").strip()
                    lib_name = re.sub(r"\s+", " ", lib_name).strip()
                    break

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = raw_title
                book.author = base_author
                book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                book.call_number = call_no
                book.location = ""
                
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("양주시", YangjuScraper, metro_name="경기도")
register_scraper("양주시립도서관", YangjuScraper, metro_name="경기도")


# ========================================================================
# 여주시 도서관 - 포털 기반 전용 스크래퍼
# ========================================================================

class YeojuScraper(LibraryScraper):
    """여주시 도서관 실시간 검색 스크래퍼 (1차 검색 후 2차 상세페이지 소장정보 연동 기법)"""

    def __init__(self):
        super().__init__(
            region_name="여주시",
            base_url="https://www.yjlib.go.kr/web/menu/10036/program/30001/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchType": "SIMPLE",
            "searchLibrary": "ALL",
            "searchCategory": "ALL",
            "searchField": "ALL",
            "searchWord": query
        }

        try:
            resp = self._session.post(self.base_url, data=payload, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 여주시 도서관 1차 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 전체 검색 건수 파싱
        total_count = 0
        cnt_tag = soup.select_one(".result_screen strong.highlight:nth-of-type(2), strong.highlight")
        if cnt_tag:
            try:
                total_count = int(re.sub(r"[^\d]", "", cnt_tag.text))
            except ValueError:
                pass

        # 도서 상세 링크와 고유 식별자 수집
        # onclick="fnSearchResultDetail('speciesKey','bookKey','BO');"
        detail_items = soup.select("a[onclick*='fnSearchResultDetail']")
        if not detail_items:
            return 0, []

        books = []
        seen_keys = set()
        
        # 속도 최적화를 위해 상위 8건만 상세페이지 요청
        for a in detail_items:
            onclick_text = a.get("onclick", "")
            match = re.search(r"fnSearchResultDetail\s*\(\s*['\"]?(\d+)['\"]?\s*,\s*['\"]?(\d+)['\"]?\s*,\s*['\"]?(\w+)['\"]?", onclick_text)
            if not match:
                continue
            
            species_key, book_key, pub_code = match.groups()
            key_pair = (species_key, book_key)
            if key_pair in seen_keys:
                continue
            seen_keys.add(key_pair)

            if len(seen_keys) > 8:
                break

            # 1차 도서명 수집
            raw_title = ""
            title_tag = a.find_parent("div", class_="book_name")
            if title_tag:
                raw_title = title_tag.text.strip()
            else:
                # 썸네일 이미지 링크에서 부모 탐색
                parent_li = a.find_parent("li")
                if parent_li:
                    name_div = parent_li.select_one(".book_name")
                    if name_div:
                        raw_title = name_div.text.strip()

            raw_title = re.sub(r"^\s*\[.*?\]\s*", "", raw_title)  # 접두종류 제거
            raw_title = re.sub(r"^\d+\.\s*", "", raw_title).strip()

            # 1차 저자 수집
            raw_author = ""
            parent_li = a.find_parent("li")
            if parent_li:
                info_div = parent_li.select_one(".book_info")
                if info_div:
                    raw_author = info_div.text.strip()
                    raw_author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", raw_author).strip()

            # 2차 상세페이지 호출
            d_url = "https://www.yjlib.go.kr/web/menu/10036/program/30001/searchResultDetail.do"
            d_payload = {
                "speciesKey": species_key,
                "bookKey": book_key,
                "publishFormCode": pub_code,
                "searchType": "SIMPLE",
                "searchMenuCategory": "ALL"
            }

            try:
                d_resp = self._session.post(d_url, data=d_payload, headers=self._headers, timeout=8, verify=False)
                if d_resp.status_code == 200:
                    dsoup = BeautifulSoup(d_resp.text, "html.parser")
                    tables = dsoup.select("table")
                    for table in tables:
                        headers = [th.text.strip() for th in table.select("th")]
                        if any(h in "".join(headers) for h in ["도서관", "청구기호", "소장처"]):
                            rows = table.select("tbody tr")
                            for row in rows:
                                tds = row.select("td")
                                if len(tds) >= 4:
                                    # 셀 인덱스: 도서관 | 도서상태 | 청구기호 | 등록번호 | ... | 소장처
                                    raw_lib = tds[0].text.strip()
                                    call_no = tds[2].text.strip()
                                    # 소장처는 마지막 또는 5번째 셀
                                    loc_name = tds[-1].text.strip() if len(tds) > 4 else ""

                                    # 도서관 지점명 가공 (예: "[여주][세종]관" -> "여주세종도서관")
                                    lib_name = re.sub(r"[\[\]\s]", "", raw_lib)
                                    if lib_name.endswith("관"):
                                        lib_name = lib_name[:-1] + "도서관"
                                    if not lib_name.endswith("도서관"):
                                        lib_name += "도서관"

                                    call_no = re.sub(r"\s+", " ", call_no).strip()

                                    if lib_name and call_no:
                                        book = BookInfo(region="경기도")
                                        book.title = raw_title
                                        book.author = raw_author
                                        book.library = lib_name
                                        book.call_number = call_no
                                        book.location = loc_name
                                        
                                        books.append(book)
            except Exception:
                pass

        return total_count if total_count > 0 else len(books), books

register_scraper("여주시", YeojuScraper, metro_name="경기도")
register_scraper("여주시립도서관", YeojuScraper, metro_name="경기도")


# ========================================================================
# 동두천시 도서관 - 포털 iframe 기반 전용 스크래퍼
# ========================================================================

class DongducheonScraper(LibraryScraper):
    """동두천시 도서관 실시간 검색 스크래퍼 (다중 지점코드 동시 조립 및 1차 검색결과 수집 기법)"""

    def __init__(self):
        super().__init__(
            region_name="동두천시",
            base_url="https://lib.ddc.go.kr/kolaseek/plus/search/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        
        # 동두천시 관내 지점 코드 목록
        libs_arr = ["MA", "MC", "MB", "SB", "SE"]
        
        params = []
        for code in libs_arr:
            params.append(("searchLibraryArr", code))
        
        params.extend([
            ("searchKeyword", query),
            ("searchType", "SIMPLE"),
            ("searchCategory", "ALL"),
            ("searchKey", "ALL")
        ])

        try:
            resp = self._session.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 동두천시 도서관 통합검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 전체 검색 건수 파싱
        total_count = 0
        cnt_tag = soup.select_one("strong.searcKwd ~ span.themeFC, strong.searcKwd ~ b.themeFC")
        if not cnt_tag:
            cnt_tag = soup.select_one("span.themeFC")
        if cnt_tag:
            try:
                total_count = int(re.sub(r"[^\d]", "", cnt_tag.text))
            except ValueError:
                pass

        book_items = soup.select("dl.bookDataWrap")
        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            # 제목
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            raw_title = title_tag.text.strip()
            # 접두 숫자 제거
            raw_title = re.sub(r"^\d+\.\s*", "", raw_title)

            # 저자
            base_author = ""
            author_tag = item.select_one("dd.author span")
            if author_tag:
                base_author = author_tag.text.strip()
                # "저자 : ", "저 : " 제거
                base_author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", base_author)

            # 청구기호
            call_no = ""
            data_spans = item.select("dd.data span")
            for span in data_spans:
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").replace("위치", "").strip()
                    call_no = re.sub(r"\s+", " ", call_no).strip()
                    break

            # 도서관명
            lib_name = ""
            site_spans = item.select("dd.site span")
            for span in site_spans:
                txt = span.text.strip()
                if "관:" in txt or "도서관" in txt or "관 " in txt:
                    lib_name = txt.replace("관", "").replace(":", "").strip()
                    lib_name = re.sub(r"\s+", " ", lib_name).strip()
                    break

            # 도서관명 후가공
            if lib_name:
                lib_name = re.sub(r"[\[\]\s]", "", lib_name)
                # 예: "시립" -> "동두천시립도서관", "꿈나무" -> "꿈나무도서관"
                if "시립" in lib_name:
                    lib_name = "동두천시립도서관"
                else:
                    if not lib_name.endswith("도서관"):
                        lib_name += "도서관"

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = raw_title
                book.author = base_author
                book.library = lib_name
                book.call_number = call_no
                book.location = ""
                
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("동두천시", DongducheonScraper, metro_name="경기도")
register_scraper("동두천시립도서관", DongducheonScraper, metro_name="경기도")


# ========================================================================
# 가평군 도서관 - 포털 기반 전용 스크래퍼
# ========================================================================

class GapyeongScraper(LibraryScraper):
    """가평군 도서관 실시간 검색 스크래퍼 (포털 기반 단일 GET 통신 및 1차 검색결과 수집 기법)"""

    def __init__(self):
        super().__init__(
            region_name="가평군",
            base_url="http://www.gaplib.go.kr/intro/menu/10035/program/30005/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('http://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        
        # 가평군 관내 주요 지점 코드 목록 전수 빌딩
        libs_arr = ["MA", "MC", "MD", "MB"]
        
        params = []
        for code in libs_arr:
            params.append(("searchLibraryArr", code))
            
        params.extend([
            ("searchKeyword", query),
            ("searchType", "SIMPLE"),
            ("searchCategory", "ALL"),
            ("searchKey", "ALL")
        ])

        try:
            resp = self._session.get(self.base_url, params=params, headers=self._headers, timeout=12, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 가평군 도서관 통합검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 전체 검색 건수 파싱
        total_count = 0
        cnt_tag = soup.select_one("strong.searcKwd ~ span.themeFC, strong.searcKwd ~ b.themeFC")
        if not cnt_tag:
            cnt_tag = soup.select_one("span.themeFC")
        if cnt_tag:
            try:
                total_count = int(re.sub(r"[^\d]", "", cnt_tag.text))
            except ValueError:
                pass

        book_items = soup.select("dl.bookDataWrap")
        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            # 제목
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            raw_title = title_tag.text.strip()
            raw_title = re.sub(r"^\d+\.\s*", "", raw_title)

            # 저자
            base_author = ""
            author_tag = item.select_one("dd.author span")
            if author_tag:
                base_author = author_tag.text.strip()
                base_author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", base_author)

            # 청구기호
            call_no = ""
            data_spans = item.select("dd.data span")
            for span in data_spans:
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").replace("위치", "").strip()
                    call_no = re.sub(r"\s+", " ", call_no).strip()
                    break

            # 도서관명
            lib_name = ""
            site_spans = item.select("dd.site span")
            for span in site_spans:
                txt = span.text.strip()
                if "관:" in txt or "도서관" in txt or "관 " in txt:
                    lib_name = txt.replace("관", "").replace(":", "").strip()
                    lib_name = re.sub(r"\s+", " ", lib_name).strip()
                    break

            # 가평 도서관명 후가공
            if lib_name:
                lib_name = re.sub(r"[\[\]\s]", "", lib_name)
                # 예: "한석봉" -> "한석봉도서관", "가평" -> "가평도서관"
                if not lib_name.endswith("도서관"):
                    lib_name += "도서관"

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = raw_title
                book.author = base_author
                book.library = lib_name
                book.call_number = call_no
                book.location = ""
                
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("가평군", GapyeongScraper, metro_name="경기도")
register_scraper("가평군립도서관", GapyeongScraper, metro_name="경기도")


class UiwangScraper(LibraryScraper):
    """의왕시 도서관 스크래퍼 (uwlib.or.kr)"""
    def __init__(self):
        super().__init__(
            region_name="의왕시",
            base_url="https://www.uwlib.or.kr/jungang/program/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchType": "SIMPLE",
            "searchCategory": "ALL",
            "searchField": "ALL",
            "searchWord": query,
            "searchLibrary": "ALL",
            "searchPbLibrary": "ALL",
            "searchSmLibrary": "ALL",
            "pageIndex": 1
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.uwlib.or.kr/intro/index.do',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            self._session.get("https://www.uwlib.or.kr/intro/index.do", headers=headers, timeout=8, verify=False)
        except Exception:
            pass

        try:
            r = self._session.post(self.base_url, data=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 의왕시 도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        books = []
        items = soup.select("ul.listWrap > li:not(.noResultNote)")
        
        for item in items:
            data_inner = item.select_one("div.book_dataInner")
            if not data_inner:
                continue

            title_tag = data_inner.select_one("div.book_name a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            book_title = re.sub(r"^(도서|서양서|비도서|잡지)\s*", "", book_title).strip()

            author_div = data_inner.select_one("div.info01 div")
            book_author = author_div.text.strip() if author_div else ""
            book_author = re.sub(r"\s*지음|\s*저|\s*옮김", "", book_author).strip()

            publisher = ""
            pub_year = ""
            call_no = ""
            info02_p = data_inner.select("div.info02 div p")
            if len(info02_p) >= 1:
                publisher = info02_p[0].text.strip()
            if len(info02_p) >= 2:
                pub_year = info02_p[1].text.strip()
            if len(info02_p) >= 3:
                call_no = info02_p[2].text.strip()

            lib_name = "의왕시도서관"
            location = ""
            info03_p = data_inner.select("div.info03 div p")
            if len(info03_p) >= 1:
                lib_name = info03_p[0].text.strip()
            if len(info03_p) >= 2:
                location = info03_p[1].text.strip()

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                book.location = location
                
                books.append(book)

        return len(books), books

register_scraper("의왕시", UiwangScraper, metro_name="경기도")
register_scraper("의왕시도서관", UiwangScraper, metro_name="경기도")


class AnseongScraper(LibraryScraper):
    """안성시립도서관 스크래퍼 (anseong.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="안성시",
            base_url="https://www.anseong.go.kr/library/search/search.do?mId=0101010100"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())
        self.api_url = "https://www.anseong.go.kr/library/search/biblioSearch.do"

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchKeyType": "K",
            "searchTxt": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.anseong.go.kr/library/main.do'
        }

        try:
            r = self._session.post(self.base_url, data=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 안성시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        dls = soup.select("div.anseong-search-list-table dl")
        
        books = []
        for dl in dls:
            title_tag = dl.select_one("dd > a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            
            author_tag = dl.select_one("dd > span")
            book_author = ""
            if author_tag:
                txt = author_tag.text.strip()
                lines = [line.strip() for line in txt.split("\n") if line.strip()]
                book_author = lines[0] if lines else ""
                book_author = re.sub(r"\[.*?\]", "", book_author).strip()

            # biblioId 및 branchId 추출
            biblio_id = None
            branch_id = None
            for a_btn in dl.select("a, button"):
                onc = a_btn.get("onclick", "")
                m = re.search(r"biblioSearch\(\s*(\d+(?:\.\d+)?)\s*,\s*['\"]?[^'\"]*['\"]?\s*,\s*(\d+)", onc)
                if m:
                    biblio_id = str(int(float(m.group(1))))
                    branch_id = m.group(2)
                    break
                # goView fallback
                if not biblio_id:
                    m2 = re.search(r"goView\(\s*(\d+(?:\.\d+)?)", onc)
                    if m2:
                        biblio_id = str(int(float(m2.group(1))))
            
            if not biblio_id:
                continue

            # API 호출하여 소장 정보 파싱
            try:
                api_data_payload = {"biblioId": biblio_id}
                if branch_id:
                    api_data_payload["branchId"] = branch_id

                api_resp = self._session.post(
                    self.api_url,
                    data=api_data_payload,
                    headers=headers,
                    timeout=6,
                    verify=False
                )
                if api_resp.status_code == 200:
                    api_data = api_resp.json()
                    if api_data.get("success"):
                        items = api_data.get("data", {}).get("list", [])
                        for item in items:
                            branch_name = item.get("branch", {}).get("name", "안성시립도서관")
                            loc_name = item.get("location", {}).get("name", "")
                            call_no = item.get("callNo", "")
                            
                            if branch_name and call_no:
                                book = BookInfo(region="경기도")
                                book.title = book_title
                                book.author = book_author
                                book.library = branch_name
                                book.call_number = call_no
                                book.location = loc_name
                                books.append(book)
            except Exception as e:
                pass

        return len(books), books

register_scraper("안성시", AnseongScraper, metro_name="경기도")
register_scraper("안성시립도서관", AnseongScraper, metro_name="경기도")


class YeoncheonScraper(LibraryScraper):
    """연천군 도서관 스크래퍼 (library.yeoncheon.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="연천군",
            base_url="https://library.yeoncheon.go.kr/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchType": "SIMPLE",
            "searchCategory": "ALL",
            "searchKey": "TITLE",
            "searchKeyword": query,
            "searchWordTitle": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.yeoncheon.go.kr/index.do'
        }

        try:
            self._session.get("https://library.yeoncheon.go.kr/index.do", headers=headers, timeout=8, verify=False)
        except Exception:
            pass

        try:
            r = self._session.post(self.base_url, data=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 연천군 도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("dl.bookDataWrap")

        books = []
        for item in items:
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            book_title = re.sub(r"^(도서|비도서|서양서|잡지)\s*", "", book_title).strip()
            book_title = re.sub(r"^\d+\.\s*", "", book_title).strip()

            book_author = ""
            author_dd = item.select_one("dd.author")
            if author_dd:
                txt = author_dd.text.strip()
                m = re.search(r"저자\s*:\s*([^발행년도발행자]+)", txt)
                if m:
                    book_author = m.group(1).strip()
                    book_author = re.sub(r"지은이:\s*|\s*지음|\s*저", "", book_author).strip()

            call_no = ""
            data_dd = item.select_one("dd.data")
            if data_dd:
                txt = data_dd.text.strip()
                m = re.search(r"청구기호\s*:\s*([^\s위치출력]+)", txt)
                if m:
                    call_no = m.group(1).strip()

            lib_name = "연천군도서관"
            location = ""
            site_dd = item.select_one("dd.site")
            if site_dd:
                txt = site_dd.text.strip()
                m_lib = re.search(r"도서관\s*:\s*([^\s자료실]+)", txt)
                if m_lib:
                    lib_name = m_lib.group(1).strip()
                m_loc = re.search(r"자료실\s*:\s*([^\s부록]+)", txt)
                if m_loc:
                    location = m_loc.group(1).strip()

            if lib_name and call_no:
                book = BookInfo(region="경기도")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                book.location = location
                books.append(book)

        return len(books), books

register_scraper("연천군", YeoncheonScraper, metro_name="경기도")
register_scraper("연천군도서관", YeoncheonScraper, metro_name="경기도")


class GunpoScraper(LibraryScraper):
    """군포시 도서관 스크래퍼 (gunpolib.go.kr - Pyxis API 연동)"""
    def __init__(self):
        super().__init__(
            region_name="군포시",
            base_url="https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "all": f"k|a|{query}",
            "max": 20
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.gunpolib.go.kr/'
        }

        try:
            self._session.get("https://www.gunpolib.go.kr/", headers={'User-Agent': headers['User-Agent']}, timeout=8, verify=False)
        except Exception:
            pass

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"  [오류] 군포시 도서관 검색 실패: {e}")
            return 0, []

        if not data.get("success") or "data" not in data or "list" not in data["data"]:
            return 0, []

        total_count = data["data"].get("totalCount", 0)
        items = data["data"]["list"]

        books = []
        for item in items:
            book_title = item.get("titleStatement", "").strip()
            book_title = re.sub(r"^\(.*?\)\s*", "", book_title).strip()
            
            book_author = item.get("author", "").strip()
            
            branch_vols = item.get("branchVolumes", [])
            if not branch_vols:
                # branchVolumes가 없는 경우 기본 항목 처리
                book = BookInfo(region="경기도")
                book.title = book_title
                book.author = book_author
                book.library = "군포시도서관"
                book.call_number = ""
                books.append(book)
            else:
                for vol in branch_vols:
                    lib_name = vol.get("name", "군포시도서관")
                    if not lib_name.endswith("도서관"):
                        lib_name += "도서관"
                    call_no = vol.get("volume", "").strip()

                    if lib_name:
                        book = BookInfo(region="경기도")
                        book.title = book_title
                        book.author = book_author
                        book.library = lib_name
                        book.call_number = call_no
                        books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("군포시", GunpoScraper, metro_name="경기도")
register_scraper("군포시도서관", GunpoScraper, metro_name="경기도")


class SiheungScraper(LibraryScraper):
    """시흥시 도서관 스크래퍼 (lib.siheung.go.kr - Pyxis API 연동)"""
    def __init__(self):
        super().__init__(
            region_name="시흥시",
            base_url="https://lib.siheung.go.kr/pyxis-api/1/collections/1/search"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "all": f"k|a|{query}",
            "max": 20
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://lib.siheung.go.kr/'
        }

        try:
            self._session.get("https://lib.siheung.go.kr/", headers={'User-Agent': headers['User-Agent']}, timeout=8, verify=False)
        except Exception:
            pass

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"  [오류] 시흥시 도서관 검색 실패: {e}")
            return 0, []

        if not data.get("success") or "data" not in data or "list" not in data["data"]:
            return 0, []

        total_count = data["data"].get("totalCount", 0)
        items = data["data"]["list"]

        books = []
        for item in items:
            book_title = item.get("titleStatement", "").strip()
            book_title = re.sub(r"^\(.*?\)\s*", "", book_title).strip()
            
            book_author = item.get("author", "").strip()
            
            branch_vols = item.get("branchVolumes", [])
            if not branch_vols:
                book = BookInfo(region="경기도")
                book.title = book_title
                book.author = book_author
                book.library = "시흥시도서관"
                book.call_number = ""
                books.append(book)
            else:
                for vol in branch_vols:
                    lib_name = vol.get("name", "시흥시도서관")
                    if not lib_name.endswith("도서관"):
                        lib_name += "도서관"
                    call_no = vol.get("volume", "").strip()

                    if lib_name:
                        book = BookInfo(region="경기도")
                        book.title = book_title
                        book.author = book_author
                        book.library = lib_name
                        book.call_number = call_no
                        books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("시흥시", SiheungScraper, metro_name="경기도")
register_scraper("시흥시도서관", SiheungScraper, metro_name="경기도")


class BucheonScraper(LibraryScraper):
    """부천시립도서관 스크래퍼 (bcl.go.kr - AlpasQ API 연동)"""
    def __init__(self):
        super().__init__(
            region_name="부천시",
            base_url="https://alpasq.bcl.go.kr/api/search"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchKeyword": query,
            "page": 1,
            "display": 20,
            "manageCode": "ALL"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://alpasq.bcl.go.kr/'
        }

        try:
            r = self._session.post(self.base_url, json=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"  [오류] 부천시립도서관 검색 실패: {e}")
            return 0, []

        contents = data.get("contents", {})
        total_count = contents.get("totalCount", 0)
        items = contents.get("bookList", [])

        books = []
        for item in items:
            book_title = item.get("originalTitle") or item.get("title", "")
            book_title = re.sub(r"<[^>]+>", "", book_title).strip()
            
            book_author = item.get("originalAuthor") or item.get("author", "")
            book_author = re.sub(r"\s*저\.?|\s*지음", "", book_author).strip()

            lib_name = item.get("libName", "부천시립도서관")
            if not lib_name.endswith("도서관"):
                lib_name += "도서관"

            call_no = item.get("callNo", "").strip()
            location = item.get("shelfLocName", "").strip()

            if lib_name:
                book = BookInfo(region="경기도")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                book.location = location
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("부천시", BucheonScraper, metro_name="경기도")
register_scraper("부천시립도서관", BucheonScraper, metro_name="경기도")


# ========================================================================
# 고양시 도서관 - 도서관센터 통합 검색 스크래퍼
# ========================================================================

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

                info02_spans = b.select('.info02 p.kor span, .info02 span')
                call_no = ""
                if len(info02_spans) >= 3:
                    call_no = info02_spans[2].text.strip()
                elif len(info02_spans) == 2:
                    call_no = info02_spans[1].text.strip()

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
                
                all_books.append(book)

            if total_count == 0:
                total_count = len(all_books)

            if len(all_books) >= total_count or len(book_areas) < display_num:
                break

            page += 1

        return total_count, all_books

register_scraper("고양시", GoyangScraper, metro_name="경기도")
register_scraper("고양시도서관", GoyangScraper, metro_name="경기도")


# ========================================================================
# 미확인 사이트 (GenericLibraryScraper - 빈 결과 반환)
# ========================================================================

UNIMPLEMENTED_GYEONGGI = [
    "광주시"
]

for city_name in UNIMPLEMENTED_GYEONGGI:
    class _Scraper(GenericLibraryScraper):
        def __init__(self, cname=city_name):
            super().__init__(region_name=cname, metro_name="경기도")

    register_scraper(city_name, _Scraper, metro_name="경기도")








