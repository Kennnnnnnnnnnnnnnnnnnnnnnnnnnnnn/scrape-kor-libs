"""
스크래퍼 레지스트리 - 광역단위 및 지역/도서관별 스크래퍼 등록 및 관리
"""
from typing import Dict, Tuple, List, Optional
from .base import LibraryScraper

# 광역단위 -> {지역/도서관명: 스크래퍼 클래스 또는 인스턴스 팩토리}
_METRO_REGISTRY: Dict[str, Dict[str, type[LibraryScraper]]] = {}

# 단일 지역 이름 -> (광역단위, 스크래퍼 클래스) 역방향 인덱스
_NAME_TO_METRO: Dict[str, str] = {}


# 대한민국 광역단위 및 하위 지원 도서관 정의
METRO_MAP = {
    "경기도": [
        "수원시", "성남시", "고양시", "용인시", "부천시", "안산시", "안양시", "남양주시",
        "화성시", "평택시", "의정부시", "파주시", "시흥시", "김포시", "광명시", "광주시",
        "군포시", "하남시", "오산시", "양주시", "이천시", "구리시", "안성시", "포천시",
        "의왕시", "양평군", "여주시", "동두천시", "가평군", "과천시", "연천군"
    ],
    "서울특별시": [
        "서울도서관", "서울시교육청도서관", "강남구립도서관", "강동구립도서관", "강북구립도서관",
        "관악구립도서관", "광진구립도서관", "구로구립도서관", "금천구립도서관", "노원구립도서관",
        "도봉구립도서관", "동대문구립도서관", "동작구립도서관", "마포구립도서관", "서대문구립도서관",
        "서초구립도서관", "성동구립도서관", "성북구립도서관", "송파구립도서관", "양천구립도서관",
        "영등포구립도서관", "용산구립도서관", "은평구립도서관", "종로구립도서관", "중구립도서관", "중랑구립도서관"
    ],
    "부산광역시": [
        "부산도서관", "부산광역시립시민도서관", "해운대구립도서관", "금정구립도서관", "사하구립도서관"
    ],
    "대구광역시": [
        "대구광역시립도서관통합포털", "수성구립도서관", "달서구립도서관"
    ],
    "인천광역시": [
        "미추홀도서관", "인천광역시교육청도서관", "부평구립도서관", "연수구립도서관"
    ],
    "광주광역시": [
        "광주광역시립도서관", "광산구립도서관", "남구립도서관"
    ],
    "대전광역시": [
        "한밭도서관", "서구립도서관", "유성구립도서관"
    ],
    "울산광역시": [
        "울산도서관", "북구립도서관", "울주군립도서관"
    ],
    "세종특별자치시": [
        "세종특별자치시립도서관"
    ],
    "강원특별자치도": [
        "강원특별자치도교육청도서관", "춘천시립도서관", "강릉시립도서관", "원주시립도서관"
    ],
    "충청북도": [
        "청주시립도서관", "충주시립도서관", "제천시립도서관"
    ],
    "충청남도": [
        "충청남도도서관", "천안시도서관", "아산시립도서관", "논산시립도서관"
    ],
    "전북특별자치도": [
        "전북도서관", "전주시립도서관", "군산시립도서관", "익산시립도서관"
    ],
    "전라남도": [
        "전라남도립도서관", "목포시립도서관", "여수시립도서관", "순천시립도서관"
    ],
    "경상북도": [
        "경상북도교육청대표도서관", "포항시립도서관", "구미시립도서관", "경주시립도서관"
    ],
    "경상남도": [
        "경상남도대표도서관", "창원시립도서관", "김해시립도서관", "진주시립도서관"
    ],
    "제주특별자치도": [
        "제주도립도서관", "한라도서관", "우당도서관", "탐라도서관", "제주시기적의도서관", "애월도서관",
        "조천읍도서관", "한경도서관", "삼매봉도서관", "중앙도서관", "동부도서관", "서부도서관",
        "서귀포기적의도서관", "성산일출도서관", "안덕산방도서관", "표선도서관", "꿈바당어린이도서관"
    ]
}


def register_scraper(region_name: str, scraper_class: type[LibraryScraper], metro_name: str = ""):
    """지역 스크래퍼를 레지스트리에 등록합니다."""
    # 광역단위 자동 찾기
    if not metro_name:
        for m_name, reg_list in METRO_MAP.items():
            if any(region_name == r or region_name + "시" == r or region_name + "군" == r or r.startswith(region_name) for r in reg_list):
                metro_name = m_name
                break
        if not metro_name:
            metro_name = "기타"

    if metro_name not in _METRO_REGISTRY:
        _METRO_REGISTRY[metro_name] = {}

    _METRO_REGISTRY[metro_name][region_name] = scraper_class
    _NAME_TO_METRO[region_name] = metro_name


def get_scraper(region_name: str, metro_name: str = "") -> LibraryScraper:
    """지역 이름(및 광역단위 이름)으로 스크래퍼 인스턴스를 반환합니다."""
    # 1. 완벽 일치 검색
    if metro_name and metro_name in _METRO_REGISTRY and region_name in _METRO_REGISTRY[metro_name]:
        return _METRO_REGISTRY[metro_name][region_name]()

    # 2. 광역 관계없이 region_name 찾기
    for m_name, sub_dict in _METRO_REGISTRY.items():
        if region_name in sub_dict:
            return sub_dict[region_name]()
        # 접미사 (시/군) 호환
        for key, scraper_cls in sub_dict.items():
            if key.startswith(region_name) or region_name.startswith(key):
                return scraper_cls()

    # 3. 범용 GenericScraper 반환 (기본 통합 스크래퍼)
    from .generic import GenericLibraryScraper
    return GenericLibraryScraper(region_name, metro_name)


def get_metro_map() -> Dict[str, List[str]]:
    """광역단위별 지역 도서관 맵을 반환합니다."""
    return METRO_MAP


def find_metro_by_region(region_name: str) -> str:
    """지역/도서관 이름으로 광역단위 이름을 탐색합니다."""
    clean_reg = region_name.strip()
    for metro, lib_list in METRO_MAP.items():
        for lib in lib_list:
            if clean_reg == lib or clean_reg + "시" == lib or clean_reg + "군" == lib or lib.startswith(clean_reg):
                return metro
    return "기타"
