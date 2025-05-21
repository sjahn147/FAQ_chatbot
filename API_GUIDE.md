# FAQ 챗봇 API 가이드

## API 엔드포인트

### 1. 챗봇 대화
```
POST /api/chat
```

#### 요청 예시
```json
{
    "message": "학습은 어떻게 시작하나요?",
    "session_id": "user123"  // 선택사항
}
```

#### 응답 예시
```json
{
    "response": "정규과정 학습은 계획표를 확인하는 것으로 시작됩니다...",
    "session_id": "user123"
}
```

### 2. Q&A 관리
```
GET /api/qa  # Q&A 목록 조회
POST /api/qa  # Q&A 추가
PUT /api/qa/{qa_id}  # Q&A 수정
DELETE /api/qa/{qa_id}  # Q&A 삭제
```

## 사용 방법

1. 서버 실행
```bash
# 개발 환경
uvicorn app.main:app --reload

# 프로덕션 환경
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. API 테스트
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 환경 설정

1. .env 파일 설정
```
CLAUDE_API_KEY=your_api_key_here
ENVIRONMENT=development
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 주의사항

1. API 키 관리
- API 키는 반드시 .env 파일에 저장
- .env 파일은 절대 Git에 커밋하지 않기

2. 세션 관리
- session_id를 사용하여 대화 컨텍스트 유지
- 세션은 30분 후 자동 만료

3. 에러 처리
- 400: 잘못된 요청
- 401: 인증 실패
- 404: 리소스 없음
- 500: 서버 에러 