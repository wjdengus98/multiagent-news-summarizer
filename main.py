"""네이버 뉴스 AI 멀티에이전트 시스템 - 메인 실행 파일"""
import os
import asyncio
import logging
from datetime import datetime

from workflow import create_news_workflow
from config import Config
from state import NewsState

# 로거 설정 - 시스템 실행 중 발생하는 이벤트 오류 추적
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    """네이버 뉴스 처리 메인 함수
    네이버 뉴스 수집 -> AI 요약 -> 카테고리 분류 -> 마크다운 보고서 생성
    """

    # 설정 검증
    try:
        if not Config.validate():
            raise ValueError("OPENAI_API 키가 설정되지 않았습니다. .env 파일을 확인해주세요")
        
        # 워크플로 생성
        app = create_news_workflow()
        
        # 워크플로 실행  
        initial_state = NewsState()
        final_state = await app.ainvoke(initial_state)
        
        # 보고서 저장
        if not final_state.get("final_report"):
            print("생성된 보고서가 없습니다.")
            return
        
        # 출력 디렉토리 설정
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        
        # 파일명 생성 (타임스탬프 포함)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(Config.OUTPUT_DIR, f"news_report_{timestamp}.md")
        
        # 파일 저장
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_state["final_report"])
        
        # 결과 출력
        print("\n" + "=" * 60)
        print("처리 완료")
        print("=" * 60)
        print(f"\n보고서가 저장되었습니다: {filename}")
        print(f"처리된 뉴스: {len(final_state.get('summarized_news', []))}건")
        
        #보고서 미리보기
        print("\n 보고서 미리보기:")
        print("-" * 60)
        preview = final_state["final_report"]
        print(preview)
        
        # 예외 처리 - 사용자 중단과 일반 오류를 구분하여 처리
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.exception("실행 중 오류 발생")
        print(f"\n오류 발생: {e}")

# 프로그램 진입점 - 비동기 메인 함수 실행
if __name__ == "__main__":
    asyncio.run(main())
    

        
         