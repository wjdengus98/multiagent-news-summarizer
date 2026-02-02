from typing import Annotated, Any
from pydantic import BaseModel, ConfigDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class NewsState(BaseModel):
    """뉴스 처리 상태를 관리하는 BaseModel"""
    
    # 1. Pydantic이 모르는 타입을 허용
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # 2. 대화의 히스토리 저장을 위한 필드
    messages: Annotated[list[BaseMessage], add_messages] = []
    
    # 3. RSS 수집 단계 - 원본 뉴스 데이터
    raw_news: list[dict[str,Any]] = []
    
    # 4. 요약 단계 - AI로 요약된 뉴스
    summarized_news: list[dict[str,Any]] = []
    
    # 5. 분류 단계 - 카테고리컬로 분류된 뉴스
    categorized_news: dict[str, list[dict[str,Any]]] = {}
    
    #6. 리포트를 문자열로 저장
    fianl_report: str =""
    
    #7. 에러를 기록
    error_log: list[str] = []
    