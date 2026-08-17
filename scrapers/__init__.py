# 공공도서관 스크래퍼 패키지
from .base import LibraryScraper, BookInfo
from .registry import (
    get_scraper,
    register_scraper,
    get_metro_map,
    find_metro_by_region,
    METRO_MAP
)

# 개별 구현 스크래퍼 (우선 로드)
from . import hwaseong
from . import yongin
from . import anyang
from . import busan
from . import jeju
from . import seoullib
from . import seongbuklib

# jnet 통합 스크래퍼 모듈
from . import jnet

# 광역단위 스크래퍼 모듈 자동 등록
from . import gyeonggi
from . import goyang
from . import seoul
from . import incheon
from . import others
from . import jeonnam
from . import chungnam
from . import chungbuk


def get_available_regions() -> list[str]:
    """지원하는 모든 지역/도서관 목록 반환"""
    all_regions = []
    for metro, lib_list in METRO_MAP.items():
        all_regions.extend(lib_list)
    return all_regions
