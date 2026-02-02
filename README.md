# 🤖 Multiagent News Summarizer

LangGraph 기반 멀티 에이전트 뉴스 수집 및 요약 시스템

## 📌 프로젝트 소개

네이버 뉴스를 자동으로 수집하고, AI를 활용하여 요약 및 분류하는 멀티 에이전트 시스템입니다.

## 🎯 주요 기능

- 📰 **네이버 뉴스 자동 수집** - 6개 섹션 크롤링
- 🤖 **멀티 에이전트 시스템** - LangGraph 기반
- ✂️ **AI 요약** - OpenAI GPT-4o-mini 활용
- 🗂️ **자동 분류** - 9개 카테고리 분류
- 📊 **보고서 생성** - 마크다운 형식

## 🛠️ 기술 스택

- **LangGraph** - 멀티 에이전트 오케스트레이션
- **LangChain** - AI 워크플로우
- **OpenAI GPT-4o-mini** - 요약 및 분류
- **BeautifulSoup** - 웹 크롤링
- **Python 3.10+**

## 🏗️ 시스템 구조
```
Collector Agent → Summarizer Agent → Organizer Agent → Reporter Agent
```

## 🚀 빠른 시작
```bash
# 1. 클론
git clone https://github.com/your-username/multiagent-news-summarizer.git

# 2. 의존성 설치
uv pip install -r requirements.txt

# 3. 환경변수 설정
echo "OPENAI_API_KEY=your-key" > .env

# 4. 실행
python main.py
```

## 📁 프로젝트 구조
```
├── agents/          # 각 Agent 구현
├── config.py        # 설정 관리
├── state.py         # State 정의
├── utils.py         # 유틸리티 함수
├── workflow.py      # LangGraph 워크플로우
└── main.py          # 실행 파일
```

## 📝 License

MIT License
