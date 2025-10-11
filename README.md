
# Forwarding Assist App

![Project Banner](./regulation-frontend/public/assets/Checklist.jpg)

## 📖 프로젝트 소개

Forwarding Assist App은 국제 무역 및 물류 프로세스를 자동화하고 간소화하여 포워딩 업무를 효율적으로 처리할 수 있도록 돕는 웹 애플리케이션입니다. 사용자는 이 애플리케이션을 통해 필요한 서류를 생성하고, 규제 사항을 확인하며, 잠재적인 오류를 사전에 검사할 수 있습니다.

## ✨ 주요 기능

- **자동 문서 생성**: 상업 송장(Commercial Invoice), 포장 명세서(Packing List) 등 필수적인 무역 서류를 자동으로 생성합니다.
- **규제 정보 확인**: 각 국가 및 품목에 따른 규제 및 제한 사항을 실시간으로 조회할 수 있습니다.
- **오류 사전 검증**: 서류 작성 시 발생할 수 있는 오류나 불일치 항목을 사전에 검증하여 리스크를 최소화합니다.
- **직관적인 UI**: 사용자가 손쉽게 데이터를 입력하고 문서를 관리할 수 있는 편리한 인터페이스를 제공합니다.

## 🛠️ 기술 스택 및 아키텍처

본 프로젝트는 MSA(Microservice Architecture)를 기반으로 설계되었으며, 각 서비스는 독립적으로 개발 및 배포될 수 있습니다.

```
/
├── docker-compose.yml
├── document-generator-service/ (Python, FastAPI, PostgreSQL)
├── error-check-service/ (Python, FastAPI)
├── regulation-service/ (Python, FastAPI, MongoDB)
└── regulation-frontend/ (React)
```

- **Backend**: Python, FastAPI
- **Frontend**: React.js
- **Database**: PostgreSQL, MongoDB
- **Infrastructure**: Docker, Docker Compose

### 서비스 상세 설명

- `document-generator-service`: 템플릿과 사용자 입력을 기반으로 PDF 형식의 무역 서류를 생성합니다.
- `regulation-service`: 각국의 무역 규제 및 법규 데이터를 관리하고 API를 통해 제공합니다.
- `error-check-service`: `regulation-service`의 데이터를 기반으로 생성된 문서의 오류를 검증합니다.
- `regulation-frontend`: 전체 서비스를 위한 사용자 인터페이스를 제공하는 React 기반의 싱글 페이지 애플리케이션(SPA)입니다.

## 🚀 시작하기

프로젝트를 로컬 환경에서 실행하기 위해서는 [Docker](https://www.docker.com/get-started)가 설치되어 있어야 합니다.

1.  **프로젝트 클론**

    ```bash
    git clone https://github.com/your-username/forwarding-assist-app.git
    cd forwarding-assist-app
    ```

2.  **Docker Compose 실행**

    프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 모든 서비스를 실행합니다.

    ```bash
    docker-compose up --build
    ```

3.  **애플리케이션 접속**

    빌드가 완료되면 웹 브라우저에서 `http://localhost:3000`으로 접속하여 애플리케이션을 확인할 수 있습니다.

## ⚙️ 포트 정보

각 서비스는 다음 포트를 사용합니다.

- **Frontend**: `3000`
- **Document Generator Service**: `8000`
- **Regulation Service**: `8001`
- **Error Check Service**: `8002`

---

