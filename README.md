# FAQ 챗봇 프로젝트

## 프로젝트 개요
Claude API를 활용한 FAQ 챗봇 서비스로, Q&A 데이터를 카테고리별로 관리하고 사용자의 질문에 대해 자동으로 답변을 제공합니다.

### 주요 특징
- **데이터 관리**: 카테고리별 JSON 파일 기반 Q&A 데이터 관리
- **MVP 구현**: 검색엔진 없이 모든 Q&A를 시스템 프롬프트에 직접 포함
- **편집 도구**: PyQt 기반 Q&A JSON 편집기 제공
- **테스트 환경**: Streamlit 기반 챗봇 테스터 제공
- **API 서비스**: FastAPI 기반 RESTful API 서비스

### 기술 스택
- Backend: FastAPI, Claude API
- Frontend: Streamlit, PyQt6
- 데이터: JSON
- 개발 언어: Python 3.8+

---

## 프로젝트 구조
```
├── app/
│   ├── api/           # FastAPI 라우트
│   ├── core/          # 설정, Q&A 데이터(json), config
│   ├── services/      # Claude API 연동, Q&A 컨텍스트 처리
│   ├── tools/         # Q&A JSON 편집기(PyQt)
│   └── streamlit_app.py # Streamlit 챗봇 테스터
├── run.py             # FastAPI 실행 스크립트
├── run_streamlit.py   # Streamlit 실행 스크립트
├── requirements.txt   # 의존성 패키지 목록
└── README.md          # 프로젝트 설명서
```

---

## 설치 및 실행 방법

### 1. 환경 설정
```powershell
# 저장소 클론
git clone https://github.com/sjahn147/FAQ_chatbot.git
cd FAQ_chatbot

# 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\activate  # PowerShell/Windows

# 패키지 설치
pip install -r requirements.txt

# .env 파일 생성
# CLAUDE_API_KEY=your_api_key_here
# ENVIRONMENT=development
```

### 2. 서비스 실행
```powershell
# FastAPI 서버 실행 (8001 포트)
uvicorn app.main:app --reload --port 8001

# Q&A 편집기 실행 (별도 터미널)
python app/tools/qa_editor.py

# Streamlit 테스터 실행 (별도 터미널)
python run_streamlit.py
# 브라우저에서 http://localhost:8501 접속
```

---

## 데이터 관리

### Q&A 데이터 구조
```json
{
  "입학 관련": [
    {"question": "입학 절차가 어떻게 되나요?", "answer": "..."},
    ...
  ],
  ...
}
```

### 데이터 관리 방식
- Q&A 데이터는 `app/core/qa_data.json`에 카테고리별로 저장
- 모든 Q&A는 시스템 프롬프트에 구조화되어 포함
- **현재**: MVP 단계로 검색엔진/벡터DB 없이 모든 Q&A를 프롬프트에 직접 포함
- **향후**: Q&A가 100건 이상(10K~50K 토큰)으로 늘어나면 검색엔진/벡터DB 도입 예정

### Q&A 편집기 사용법
1. `python app/tools/qa_editor.py` 실행
2. 카테고리/질문/답변 추가, 수정, 삭제
3. 저장 버튼 클릭 시 자동으로 JSON 파일에 반영

---

## API 사용

### 1. 챗봇 대화
```
POST /api/chat
```
요청:
```json
{
    "message": "학습은 어떻게 시작하나요?",
    "context_id": "optional_context_id"
}
```
응답:
```json
{
    "response": "정규과정 학습은 계획표를 확인하는 것으로 시작됩니다...",
    "context_id": "context_id"
}
```

### 2. API 문서
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

---

## 개발/운영 시 주의사항

### 보안
- `.env` 파일은 git에 포함하지 않음 (민감정보 보호)
- API 키는 반드시 .env 파일에 저장
- 프로덕션 환경에서는 적절한 보안 설정 필요

### 데이터 관리
- Q&A 데이터는 정기적으로 백업
- 수정 전 데이터 백업 권장
- 토큰 한계(Claude 기준 약 100K 토큰) 초과 여부 주기적 확인

### 확장 계획
- **데이터 스케일업 대응**
  - Q&A가 100건 이상(10K~50K 토큰)으로 늘어나면 검색엔진/벡터DB 도입
  - SQLite, Elasticsearch, Qdrant 등 검색엔진 연동 검토
  - Redis를 활용한 자주 묻는 질문(FAQ) 캐싱으로 API 호출 비용 최적화

- **API 구조 개선**
  - 하드코딩된 추천 질문을 통한 사용자 행동 유도 및 대화 흐름 제어
  - 고정 답변이 필요한 질문은 Redis에서 즉시 반환하여 응답 시간 단축
  - API 버전 관리 및 문서화 개선

- **성능 최적화**
  - Small LLM을 활용한 질문 필터링, 카테고리 분류 등 전처리 작업 구현
  - 캐싱 전략 수립 및 구현
  - 분산처리 시스템 도입 검토

- **사용자 경험 개선**
  - 대화 히스토리 관리 기능 추가
  - 사용자 피드백 수집 및 분석 시스템 구축
  - 다국어 지원 검토

---

## 문제 해결

### 1. API 키 관련
- `.env` 파일이 올바르게 설정되었는지 확인
- API 키가 유효한지 확인

### 2. 서버 실행 문제
- 포트가 사용 중인지 확인
- 필요한 패키지가 모두 설치되었는지 확인

### 3. Q&A 데이터 문제
- JSON 형식이 올바른지 확인
- 파일 경로가 올바른지 확인

---

## 기여 및 문의
- Q&A 데이터 추가: JSON 파일 직접 편집 또는 편집기 사용
- API 엔드포인트 추가: FastAPI 라우트에 구현
- 추가 문의 및 개선 요청은 이슈 또는 메일로 연락 바랍니다 