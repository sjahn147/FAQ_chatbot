# FAQ 챗봇 프로젝트

## 프로젝트 개요
- **목표**: Claude API를 활용한 FAQ 챗봇 서비스 개발
- **주요 특징**:
  - Q&A 데이터를 카테고리별 JSON 파일로 관리
  - 별도의 검색엔진 없이 모든 Q&A를 시스템 프롬프트에 직접 포함 (MVP)
  - Q&A 데이터 편집을 위한 PyQt 기반 JSON 편집기 제공
  - Streamlit 기반 챗봇 테스터 제공
  - FastAPI 기반 RESTful API 서비스

---

## 프로젝트 구조
```
├── app/
│   ├── api/           # FastAPI 라우트
│   ├── core/          # 설정, Q&A 데이터(json), config
│   ├── services/      # Claude API 연동, Q&A 컨텍스트 처리
│   └── tools/         # Q&A JSON 편집기(PyQt)
│   └── streamlit_app.py # Streamlit 챗봇 테스터
├── run.py             # FastAPI 실행 스크립트
├── run_streamlit.py   # Streamlit 실행 스크립트
├── requirements.txt   # 의존성 패키지 목록
├── README.md          # 프로젝트 설명서
```

---

## 데이터 관리 방식
- Q&A 데이터는 `app/core/qa_data.json`에 카테고리별로 저장
- 모든 Q&A는 시스템 프롬프트에 구조화되어 포함됨
- 데이터 예시:
```json
{
  "입학 관련": [
    {"question": "입학 절차가 어떻게 되나요?", "answer": "..."},
    ...
  ],
  ...
}
```
- **MVP 단계**: 데이터가 적을 때는 검색엔진/벡터DB 없이 모든 Q&A를 프롬프트에 직접 포함
- **확장 계획**: Q&A가 수십~수백 건(예: 100건 이상, 10K~50K 토큰 이상)으로 늘어나면 검색엔진(예: SQLite, Elasticsearch, Qdrant 등) 또는 벡터DB 도입 예정

---

## Q&A JSON 편집기
- `app/tools/qa_editor.py` 실행 시 카테고리/질문/답변을 GUI로 편집 가능
- 데이터는 자동으로 JSON 파일(`app/core/qa_data.json`)에 저장됨
- 사용법: 
  1. `python app/tools/qa_editor.py` 실행
  2. 카테고리/질문/답변 추가, 수정, 삭제
  3. 저장 버튼 클릭 시 파일에 반영

---

## Streamlit 챗봇 테스터
- `run_streamlit.py` 실행 시 웹 기반 챗봇 인터페이스 제공
- 브라우저에서 `http://localhost:8501` 접속
- 실제 API 서버가 작동하지 않아도 UI 테스트 가능

---

## FastAPI 서버 실행
1. 가상환경 활성화 및 패키지 설치
2. `.env` 파일에 API 키 등 환경변수 설정
3. `uvicorn app.main:app --reload --port 8001` 명령어로 서버 실행

---

## 개발/운영 시 주의사항
- `.env` 파일은 git에 포함하지 않음(민감정보 보호)
- Q&A 데이터가 많아지면 토큰 한계(Claude 기준 약 100K 토큰) 초과 여부 확인 필요
- 데이터가 커지면 검색/벡터DB 연동 및 API 구조 개선 예정

---

## 기여 및 확장
- Q&A 데이터 추가: JSON 파일 직접 편집 또는 편집기 사용
- API 엔드포인트 추가: FastAPI 라우트에 구현
- 데이터 스케일업 시 검색/벡터DB, 캐싱, 분산처리 등 확장 가능

---

## 문의
- 추가 문의 및 개선 요청은 이슈 또는 메일로 연락 바랍니다. 

## 설치 및 실행 방법

### 1. 저장소 클론 및 디렉토리 이동
```powershell
# 저장소 클론 (예시)
git clone <repository_url>
cd 000_system/002_faq_chatbot
```

### 2. 가상환경 생성 및 활성화
```powershell
python -m venv venv
.\venv\Scripts\activate  # PowerShell/Windows
```

### 3. 패키지 설치
```powershell
pip install -r requirements.txt
```

### 4. 환경 변수 파일(.env) 생성
프로젝트 루트에 `.env` 파일을 생성하고 아래와 같이 작성하세요:
```
CLAUDE_API_KEY=your_claude_api_key_here
ENVIRONMENT=development
```

### 5. FastAPI 서버 실행
```powershell
uvicorn app.main:app --reload --port 8001
```

### 6. Q&A JSON 편집기 실행
```powershell
python app/tools/qa_editor.py
```

### 7. Streamlit 챗봇 테스터 실행
```powershell
python run_streamlit.py
# 브라우저에서 http://localhost:8501 접속
```

--- 