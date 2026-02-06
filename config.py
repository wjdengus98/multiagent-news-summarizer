"""프로젝트 설정 관리 클래스"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """프로젝트 전역 설정"""
    # ===== OPENAI 설정 =====
    # 환경변수에서 API 키를 가져오되, 없으면 빈 문자열을 기본값으로 사용
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = "gpt-4o" # 모델명 설정
    MAX_TOKENS: int = 300 # 요약 시 최대 토큰 수
    
    # ====== 프로젝트 경로 설정 ======
    # 현재 파일의 위치를 기준으로 프로젝트 루트 경로 설정
    ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
    
    # ===== 네이버 뉴스 크롤링 URLS =====
    NAVER_SECTION_URLS: dict[str, str] = {
    "정치": "https://news.naver.com/section/100",
    "경제": "https://news.naver.com/section/101",
    "사회": "https://news.naver.com/section/102",
    "생활": "https://news.naver.com/section/103",
    "세계": "https://news.naver.com/section/104",
    "IT": "https://news.naver.com/section/105",
}
    #User - Agent (봇 차단 방지)
    USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
    )
    
    #요청 타임아웃 (초)
    REQUEST_TIMEOUT: int = 10
    
    # 요청 대기 시간 (초) 
    REQUEST_DELAY: float = 1
    
    
    # ===== 수집 설정 =====
    MAX_NEWS_COUNT: int = 60
    MAX_NEWS_PER_SECTION: int = 10
    
    # ===== API 효율성 설정 =====
    BATCH_SIZE: int = 10
    
    # ===== 뉴스 카테고리 분류 설정 =====
    NEWS_CATEGORIES: list[str] = [
        "정치",
        "경제",
        "사회",
        "문화/연예",
        "IT/과학",
        "스포츠",
        "국제",
        "생활/건강",
        "기타",
    ]
    
    NEWS_PER_CATEGORY: int = 30
    
    # ===== 출력 설정 =====
    OUTPUT_DIR: str = f"{ROOT_DIR}/outputs"
    
    # ===== 설정 유효성 검사 =====
    @classmethod
    def validate(cls) -> bool:
        """설정 유효성 검사"""
        if not cls.OPENAI_API_KEY:
            print("=" * 60)
            print("❌ OpenAI API 키가 설정되지 않았습니다.")
            print("=" * 60)
            print("\n해결 방법:")
            print("1. .env 파일을 생성하고 다음 내용을 추가하세요:")
            print("   OPENAI_API_KEY=your-api-key-here")
            print("\n2. 또는 환경변수로 직접 설정하세요:")
            print("   export OPENAI_API_KEY=your-api-key-here")
            print("\n3. OpenAI API 키 발급:")
            print("   https://platform.openai.com/api-keys")
            print("=" * 60)
            return False    
        return True
    
# ===== 테스트 코드 ====== #
if __name__ =="__main__":
    # print("1. API 키 확인\n")
    # if Config.OPENAI_API_KEY:
    #     print("있음")
    # else:
    #     print("X")
    
    # 2. 모델 설정
    # print("2. OPENAI 설정: ")
    # print(f" -모델: {Config.MODEL_NAME}")
    # print(f" -토큰: {Config.NAX_TOKENS}")
    
    # 3. 네이버 RSS URL 확인
    print("네이버 RSS URL")
    for category, url in Config.NAVER_RSS_URLS.items():
        print(f" {category:4s} : {url}")

    
            

