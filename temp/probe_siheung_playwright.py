"""
Playwright 기반 시흥시도서관 통합검색 API 실시간 패킷 스니핑 진단기
"""
import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    print("=== Playwright 패킷 스니핑 시작 ===")
    async with async_playwright() as p:
        # headless=True 로 조용히 백그라운드 브라우저 구동
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 패킷 가로채기 핸들러 등록
        captured_requests = []
        
        def handle_request(request):
            url = request.url
            if "pyxis-api" in url or "search" in url or "api" in url:
                # static 자원 제외
                if not any(url.endswith(ext) for ext in [".js", ".css", ".png", ".jpg", ".woff", ".woff2"]):
                    captured_requests.append({
                        "method": request.method,
                        "url": url,
                        "headers": request.headers,
                        "post_data": request.post_data
                    })
                    
        page.on("request", handle_request)
        
        try:
            print("시흥시도서관 접속 중...")
            # 시흥시 통합검색 결과 페이지로 직접 이동 (파이썬 검색 결과 상태)
            # URL에 검색어가 실리는 구조
            target_url = "https://lib.siheung.go.kr/#/search/total?searchKeyword=%ED%8C%8C%EC%9D%B4%EC%8D%AC"
            await page.goto(target_url, timeout=30000, wait_until="networkidle")
            print("접속 및 로딩 완료. 4초간 API 응답 수집 대기...")
            await asyncio.sleep(4)
        except Exception as e:
            print("Access Error:", e)
            
        print(f"\n=== 가로챈 API 요청 목록 (총 {len(captured_requests)}건) ===")
        for i, req in enumerate(captured_requests):
            print(f"\n[{i}] {req['method']} -> {req['url']}")
            if req['post_data']:
                print(f"  PostData: {req['post_data']}")
            # 헤더 정보 중 중요한 것
            print(f"  Referer: {req['headers'].get('referer')}")
            print(f"  X-Requested-With: {req['headers'].get('x-requested-with')}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
