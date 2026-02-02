"""유틸리티 함수 모음"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import re

def clean_html(html_text:str) -> str:
    """
    HTML 태그 제거
    
    네이버 RSS의 summary 필드에 HTML 태그가 포함될 수 있어
    깨끗한 텍스트만 추출하기 위해 사용

    Args:
        html_text : HTML이 포함된 텍스트

    Returns:
        HTML이 제거된 텍스트
        
    Examples:
        >>> clean_html(<p>안녕<p>)
        "안녕"
    """
    if not html_text:
        return ""
    
    # 1. 정규표현식으로 HTML 태그 제거: <태그명>내용</태그명> 패턴 매칭
    clean_text = re.sub("<.*?>", "", html_text)
    
    # 2. 연속된 공백(스페이스, 탭, 줄바꿈)을 하나의 공백으로 정리
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    
    return clean_text

def truncate_text(text:str, max_length: int = 500) -> str:
    """
    텍스트를 적절한 길이로 자르기
    

    Args:
        text: 원본 텍스트
        max_length: 최대 길이(기본값: 500자)

    Returns:
        잘린 텍스트(필요시 "...." 추가)
    """
    if not text or len(text) <= max_length:
        return text
    
    # 지정된 길이로 자르고 말줄임표(...) 추가
    return text[:max_length] + "..."

def convert_gmt_to_kst(gmt_time_str: str) -> str:
    # Google News용 (GMT 전용)
    """GMT 시간을 KST로 변환"""
    KST_OFFSET_HOURS = 9
    gmt_time = datetime.strptime(gmt_time_str, "%a, %d %b %Y %H:%M:%S GMT")
    kst_time = gmt_time + timedelta(hours=KST_OFFSET_HOURS)
    return kst_time.strftime("%Y-%m-%d %H:%M:%S")

def convert_to_kst(date_string: str) -> str:
    """ 다양한 날짜 형식을 KST로 변환. (네이버 RSS용 추천)
        파싱 실패 시 원본 문자열 반환
    """
    try:
        # 먼저 GMT 전용 함수 시도
        if "GMT" in date_string:
            try:
                return convert_gmt_to_kst(date_string) + " KST"
            except:
                pass
        
        # RSS 표준 날짜 형식들
        # RSS 표준 날짜 형식들
        formats = [
            "%a, %d %b %Y %H:%M:%S %Z",     # Mon, 03 Feb 2025 10:30:00 GMT
            "%a, %d %b %Y %H:%M:%S %z",     # Mon, 03 Feb 2025 10:30:00 +0900
            "%Y-%m-%d %H:%M:%S",             # 2025-02-03 19:30:00
            "%Y-%m-%dT%H:%M:%S%z",           # ISO 8601 형식
        ]
        
        dt = None
        for fmt in formats:
            try:
                dt = datetime.strptime(date_string, fmt)
                break
            except ValueError:
                continue
        
        # 파싱 실패 시 원본 반환
        if dt is None:
            return date_string
        
        # 시간 대 정보가 없으면 UTC로 간주
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
            
        # KST로 변환
        kst_time = dt.astimezone(ZoneInfo("Asia/Seoul"))
        return kst_time.strftime("%Y-%m-%d %H:%M:%S KST")
    
    except Exception as e:
        print(f"⚠️ 날짜 변환 실패: {date_string} - {e}")
        return date_string

def format_number(num: int) -> str:
    """숫자를 천 단위 콤마 형식으로 변환"""
    return f"{num:,}"


def get_category_emoji(category: str) -> str:
    """카테고리에 해당하는 이모지 반환"""
    emoji_map = {
        "정치": "🏛️",
        "경제": "💰",
        "사회": "🏙️",
        "문화/연예": "🎬",
        "IT/과학": "💻",
        "스포츠": "⚽",
        "국제": "🌍",
        "생활/건강": "🏥",
        "기타": "📰",
    }
    return emoji_map.get(category, "📰")
   

# if __name__ == "__main__":
#     print(format_number(123456))