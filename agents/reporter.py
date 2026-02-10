"""최종 보고서 생성 에이전트"""
import asyncio
import sys
import os
from datetime import datetime

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import AIMessage
from dotenv import load_dotenv

from state import NewsState
from config import Config

load_dotenv()

class NewsReporterAgent:
    """최종 보고서를 생성하는 에이전트"""
    
    def __init__(self):
        self.name = "News Reporter"
        
    async def generate_report(self, state: NewsState) -> NewsState:
        """최종 보고서 생성"""
        print(f"\n[{self.name}] 보고서 생성 시작...")
        report_parts = []
        
        # 현재 시간
        current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
        
        # 처리 된 총 뉴스 수
        total_processed = sum(len(v) for v in state.categorized_news.values())
        
        #헤더
        header =f"""# 📰 네이버 뉴스 AI 요약 리포트

## 📋 기본 정보
- **수집 시간**: {current_time}
- **뉴스 소스**: 네이버 뉴스
- **수집 뉴스**: {len(state.raw_news)}건
- **처리 완료**: {total_processed}건"""
        report_parts.append(header)
        
        # 통계 섹션
        # 딕셔너리 컴프리헨션으로 각 카테고리별 뉴스 개수 집계
        category_stats = {
            cat: len(news) for cat, news in state.categorized_news.items()
        }
        
        total_news = sum(category_stats.values())
        
        if total_news > 0:
            # 마크다운 테이블 생성
            table_header = "| 카테고리 | 뉴스 수 | 비율 |\n|---------|--------|------|\n"
            
            # 뉴스 수가 많은 순으로 정렬
            table_rows = [
                f"| {cat} | {count}건 | {(count / total_news) * 100:.1f}% |"
                for cat, count in sorted(
                    category_stats.items(), key=lambda x: x[1], reverse=True
                )
                if count > 0
            ]
            
            stats_table = table_header + "\n".join(table_rows)
            stats_section = f"## 📊 카테고리별 뉴스 분포\n\n{stats_table}"
            report_parts.append(stats_section)
            
    # ===== 카테고리별 뉴스 섹션 =====
        news_sections = []
        
        for category in Config.NEWS_CATEGORIES:
            # 해당 카테고리의 뉴스 가져오기
            news_list = state.categorized_news.get(category, [])
            
            if news_list:
                section_header = f"### 📁 {category} ({len(news_list)}건)\n"
                
                # 표시할 뉴스 개수 제한
                display_count = min(len(news_list), Config.NEWS_PER_CATEGORY)
                
                # 뉴스 항목 생성
                news_items = []
                for i, news in enumerate(news_list[:display_count], 1):
                    item = f"""#### {i}. {news['title']}
- **카테고리**: {news.get('category', '미분류')}
- **요약**: {news.get('ai_summary', news.get('content', '요약 없음')[:200])}
- **링크**: [기사 보기]({news['url']})"""
                    news_items.append(item)
                
                news_items_str = "\n\n".join(news_items)
                news_sections.append(f"{section_header}\n{news_items_str}")
                
        if news_sections:
            report_parts.append(
                "## 📰 카테고리별 주요 뉴스\n\n" + "\n\n---\n\n".join(news_sections)
            )
        
        if state.error_log:
            errors = "\n".join([f"- {error}" for error in state.error_log])
            report_parts.append(f"## 처리 중 발생한 오류\n\n{errors}")
        
        # 푸터 생성
        footer = """## 참고사항
- 이 보고서는 AI(LangGraph + LangChain)를 활용하여 자동으로 생성되었습니다.
- 뉴스 요약은 OpenAI GPT 모델을 사용하여 작성되었습니다.
- 카테고리 분류는 AI가 제목과 내용을 분석하여 자동으로 수행했습니다.
- 상세한 내용은 각 뉴스의 원문 링크를 참조하시기 바랍니다."""
        report_parts.append(footer)

        # 최종 보고서 조합
        state.final_report = "\n\n---\n\n".join(report_parts)
        state.messages.append(AIMessage(content="최종 보고서가 생성되었습니다."))

        print(f"[{self.name}] 보고서 생성 완료")
        return state
    
        