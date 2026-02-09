import asyncio
import sys
import os
from typing import Dict, Any, Tuple
from collections import defaultdict

#상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from state import NewsState
from config import Config

load_dotenv()

class NewsOrganizerAgent:
    """뉴스를 카테고리별로 정리하는 에이전트"""
    
    def __init__(self):
        self.name = "News Organizer"
        
        #LLM 초기화
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            max_tokens = 50,
            temperature=0.1
        )
        
        # 카테고리 목록(기타 포함)
        self.categories = Config.NEWS_CATEGORIES
        
        # 분류 프롬프트
        system_prompt = f"""당신은 뉴스 분류 전문가 입니다.
        주어진 뉴스를 다음 카테고리 중 정확히 하나로 분류하세요:
        {", ".join(Config.NEWS_CATEGORIES)}
        
        중요:
        - 반드시 위 카테고리 중 하나만 선택
        - 카테고리 이름만 정확히 반환(설명 불필요)
        - 애매하면 가장 가까운 카테고리 선택        
        """
        
        self.categorize_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "제목: {title}\n요약: {summary}\n\n이 뉴스의 카테고리:")
            ]
        )
        
        self.chain = self.categorize_prompt | self.llm
        
    async def categorize_single_news(
        self, news_item: Dict[str,Any]
    ) -> Tuple[str, Dict[str,Any]]:
        """단일 뉴스 카테고리 판단"""
        try:
            # LLM 비동기 호출로 뉴스 분류하기
            response = await self.chain.ainvoke(
                {
                    "title":news_item["title"],
                    "summary": news_item.get("ai_summary", news_item["content"]),
                }
            )
            
            # LLM 응답에서 카테고리 추출
            category = response.content.strip()
            return category, news_item
        
        except Exception as e:
            print(f"분류 오류: {str(e)[:100]}.....")
            return "기타", news_item
    
    async def organize_news(self, state:NewsState) -> NewsState:
        """뉴스를 카테고리 별 정리"""
        print(f"📂 [{self.name}] 뉴스 분류 시작\n")
        
        summarized_news = state.summarized_news
        total_news = len(summarized_news)
        batch_size = Config.BATCH_SIZE
        
        if not summarized_news:
            print("분류할 뉴스가 없습니다.")
            return state
        
        print(f"총 {total_news}개 뉴스를 분류합니다....")
        
        #분류된 뉴스 저장용
        categorized =defaultdict(list) 
        
        # 배치 처리
        for i in range(0, total_news, batch_size):
            batch = summarized_news[i : i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total_news + batch_size - 1) // batch_size
            
            print(f" 배치 {batch_num}/{total_batches} 처리 중...")
            
            # 비동기 분류 작업
            tasks = [self.categorize_single_news(news) for news in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 처리
            for result in results:
                if isinstance(result, Exception):
                    print(f" 분류 실패: {result}")
                    continue
                
                category, news_item = result
                
                # 반환된 카테고리 유효성 검사
                if category in Config.NEWS_CATEGORIES:
                    categorized[category].append(news_item)
                else:
                    categorized["기타"].append(news_item)
                    
        print("\n 카테고리별 분포:")
            
        for category in self.categories:
            count = len(categorized.get(category, []))
                
            if count > 0:
                print(f"{category}: {count}건")
            
        state.categorized_news = dict(categorized)
        state.messages.append(
            AIMessage(content=f"뉴스를 {len(categorized)}개 카테고리로 분류했습니다.")
        )
        
        print(f"[{self.name}] 분류 완료\n")
        return state
    
    
        
                    
# if __name__ == "__main__":
    
#     # ===== 테스트 1: 단일 뉴스 분류 =====
#     async def test_single_news():
#         print("=" * 60)
#         print("테스트 1: 단일 뉴스 분류")
#         print("=" * 60)
        
#         organizer = NewsOrganizerAgent()
        
#         test_news = {
#             "title": "AI 기술의 급속한 발전",
#             "content": "인공지능 기술이 발전하고 있다.",
#             "ai_summary": "인공지능 기술이 급속히 발전하며 산업 전반에 혁신을 가져왔다.",
#         }

#         category, news_item = await organizer.categorize_single_news(test_news)
        
#         print("\n분류 결과:")
#         print(f" 카테고리: {category}")

# asyncio.run(test_single_news())
        
        