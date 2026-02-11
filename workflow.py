from langgraph.graph import StateGraph, END

from state import NewsState
from agents.collector import NaverNewsCollectorAgent
from agents.summarizer import NewsSummarizerAgent
from agents.organizer import NewsOrganizerAgent
from agents.reporter import NewsReporterAgent

def create_news_workflow() -> StateGraph:
     """뉴스 처리 워크플로우 생성 - 네이버뉴스 수집 → AI 요약 → 카테고리 분류 → 보고서 생성"""
     
     # 각 작업을 담당할 4개의 전문 에이전트 인스턴스 생성
     collector = NaverNewsCollectorAgent()
     summarizer = NewsSummarizerAgent()
     organizer = NewsOrganizerAgent()
     reporter = NewsReporterAgent()
     
     # NewsState를 state객체로 사용하는 워크플로우 생성
     workflow = StateGraph(NewsState)
     
     # 각 에이전트들의 메서드를 노드로 등록
     workflow.add_node("collect", collector.collect_news)
     workflow.add_node("summarize", summarizer.summarize_news)
     workflow.add_node("organize", organizer.organize_news)
     workflow.add_node("report", reporter.generate_report)
     
     # 워크플로우 실행 순서 정의
     workflow.set_entry_point("collect") #시작점 설정
     workflow.add_edge("collect", "summarize") #수집 -> 요약
     workflow.add_edge("summarize", "organize") # 요약 -> 분류
     workflow.add_edge("organize", "report") # 분류 -> 보고서
     workflow.add_edge("report", END) # 보고서 생성 후 종료
     
     # 워크플로우 객체 반환
     return workflow.compile()