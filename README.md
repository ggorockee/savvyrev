# 내가 쓴 리뷰 모아보기 프로젝트 (My Reviews Backend)

FastAPI를 사용하여 내가 작성한 리뷰를 한눈에 볼 수 있는 서비스의 백엔드 API입니다.

## ✨ 주요 기능

-   **사용자 인증**: JWT (JSON Web Token)을 사용한 안전한 사용자 인증 및 인가
-   **리뷰 관리**: 사용자는 본인이 작성한 리뷰를 생성하고 조회할 수 있습니다.
-   **확장 가능한 구조**: 계층형 아키텍처와 리포지토리 패턴을 적용하여 기능 추가 및 유지보수가 용이합니다.

## 🛠️ 기술 스택

-   **언어**: Python 3.11+
-   **프레임워크**: FastAPI
-   **데이터베이스**: PostgreSQL
-   **ORM**: SQLAlchemy (Asyncio 지원)
-   **데이터 유효성 검사**: Pydantic
-   **인증**: `python-jose` (JWT), `passlib` (비밀번호 해싱)
-   **환경변수 관리**: `pydantic-settings`

## 📂 프로젝트 구조

```
my-review-app/
├── app/
│   ├── main.py             # FastAPI 앱 진입점
│   ├── api/                # API 엔드포인트
│   ├── core/               # 핵심 로직 및 설정
│   ├── db/                 # 데이터베이스 설정
│   ├── models/             # SQLAlchemy 모델
│   ├── schemas/            # Pydantic 스키마
│   └── repositories/       # 리포지토리 패턴 구현
│
├── .env.example            # 환경변수 예시
├── README.md               # 프로젝트 설명서
└── requirements.txt        # 의존성 목록
```
자세한 구조는 소스 코드 내 각 디렉토리를 참고해주세요.

## 🚀 시작하기

### 1. 저장소 복제

```bash
git clone <your-repository-url>
cd my-review-app
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고, 환경에 맞게 값을 수정합니다.

```bash
cp .env.example .env
```

**`.env` 파일 내용:**
```
# PostgreSQL 연결 정보
# 형식: postgresql://[user]:[password]@[host]:[port]/[dbname]
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/myreviewdb

# JWT 설정
# 터미널에서 `openssl rand -hex 32` 명령어로 강력한 시크릿 키 생성 가능
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload
```

이제 브라우저에서 `http://127.0.0.1:8000/docs` 로 접속하여 API 문서를 확인하고 테스트할 수 있습니다.

## 🌐 API 엔드포인트

-   `POST /api/v1/login/access-token`: 로그인 및 JWT 토큰 발급
-   `POST /api/v1/reviews/`: 새로운 리뷰 생성
-   `GET /api/v1/reviews/me`: 내가 작성한 모든 리뷰 조회

---
이 프로젝트는 즐거운 코딩 경험을 위해 만들어졌습니다. 문의사항은 언제나 환영입니다! 🎉
