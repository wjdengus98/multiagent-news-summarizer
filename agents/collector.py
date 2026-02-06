"""네이버 뉴스 수집 에이전트"""
import asyncio
from typing import Optional
import sys,os
import httpx
import trafilatura
from bs4 import BeautifulSoup

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from state import NewsState

class NaverNewsCollectorAgent:
    """네이버 뉴스 섹션을 크롤링하는 에이전트"""
    def __init__(self):
        self.name = "Naver News Collector"
        self.section_urls = Config.NAVER_SECTION_URLS
        self.headers = {
            'User-Agent': Config.USER_AGENT
        }
    
    async def fetch_section_news(
        self, 
        category: str, 
        url: str, 
        max_news: int
    ) -> list[dict]:
        """
        특정 섹션에서 뉴스 목록을 가져옵니다.
        
        Args:
            category: 카테고리 이름 (예: "정치")
            url: 섹션 URL
            max_news: 수집할 최대 뉴스 수
            
        Returns:
            뉴스 정보 딕셔너리 리스트
        """
        news_list = []
        
        try:
            async with httpx.AsyncClient() as client:
                # 섹션 페이지 가져오기
                response = await client.get(
                    url,
                    headers=self.headers,
                    timeout=Config.REQUEST_TIMEOUT
                )
                
                if response.status_code != 200:
                    print(f"⚠️ {category} 섹션 접근 실패: HTTP {response.status_code}")
                    return news_list
                
                # HTML 파싱
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 뉴스 링크 찾기
                news_links = soup.select('a.sa_text_title')
                
                if not news_links:
                    print(f"{category} 섹션에서 뉴스를 찾을 수 없음")
                    return news_list
                
                print(f" {category} 섹션: {len(news_links)}개 뉴스 발견")
                
                # 지정된 개수만큼만 수집
                for link in news_links[:max_news]:
                    title = link.get_text(strip=True)
                    news_url = link.get('href', '')
                    
                    if news_url:
                        news_list.append({
                            'title': title,
                            'url': news_url,
                            'category': category
                        })
                
        except httpx.TimeoutException:
            print(f" {category} 섹션 요청 시간 초과")
        except Exception as e:
            print(f" {category} 섹션 크롤링 오류: {e}")
        
        return news_list

    async def fetch_article_content(self, news_url: str) -> Optional[str]:
        """
        개별 기사의 본문을 가져옵니다.
        
        Args:
            news_url : 뉴스 기사 URL

        Returns:
            기사 본문 텍스트 (실패 시 None)
        """
        try:
            # trafilatura로 본문 추출
            downloaded = trafilatura.fetch_url(news_url)
            
            if downloaded:
                content = trafilatura.extract(
                    downloaded,
                    include_comments=False,
                    include_images=False,
                    include_links=False,
                    target_language='ko', #한국어 최적화
                )
                return content
        except Exception as e:
            print(f"본문 추출 실패: {e}")
        return None
    
    async def parse_news_item(self, news_info: dict) -> dict:
        """
        뉴스 항목을 파싱하여 완전한 정보로 만듭니다.
        
        Args:
            news_info: 기본 뉴스 정보 (title, url, category)
            
        Returns:
            완전한 뉴스 정보 딕셔너리
        """
        # 뉴스 본문 가져오기
        content = await self.fetch_article_content(news_info['url'])
        
        await asyncio.sleep(Config.REQUEST_DELAY)
        
        result = {
            'title' : news_info['title'],
            'url' : news_info['url'],
            'category' : news_info['category'],
            'source' : "네이버뉴스",
            'content' : content
        }
        
        return result
    
    async def collect_news(self, state:NewsState) -> NewsState:
        """
        네이버 뉴스를 수집하고 상태를 업데이트합니다.
        
        Args:
            state: 현재 NewsState
            
        Returns:
            업데이트된 NewsState
        """
        print("=" * 60)
        print("네이버 뉴스 수집 시작..")
        print("=" * 60)
        
        try:
            # 섹션별 링크 수집
            tasks = [
                self.fetch_section_news(
                    category,
                    url,
                    Config.MAX_NEWS_PER_SECTION
                )
                for category, url in self.section_urls.items()
            ]
            
            section_result = await asyncio.gather(*tasks)

            # 모든 결과 합치기
            all_news = []
            for news_list in section_result:
                all_news.extend(news_list)

            print(f"총 {len(all_news)}개의 뉴스 수집 완료")
            
            total = len(all_news) # 전체 뉴스 기사의 총 갯수
            
            # 본문 수집
            raw_news = []
            batch_size = Config.BATCH_SIZE
            
            for i in range(0, total, batch_size):
                batch = all_news[i:i + batch_size]
                print(f"  처리 중: {i+1}-{min(i+batch_size, total)}/{total}")
                
                batch_tasks = [
                    self.parse_news_item(news_info)
                    for news_info in batch
                ]
                
                batch_results = await asyncio.gather(*batch_tasks)
                raw_news.extend(batch_results)
                
            #상태 업데이트
            state.raw_news = raw_news
            
            print("=" * 60)
            print(f"뉴스 수집 완료: {len(raw_news)}개")
            print("=" * 60)
        
        except Exception as e:
            error_msg = f"NaverNewsCollectorAgent: {str(e)}"
            print(f"수집 중 오류 발생: {e}")
            state.error_log.append(error_msg)
        
        return state            
    
