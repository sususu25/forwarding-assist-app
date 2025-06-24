FROM python:3.11-slim

# 시스템 의존성 설치 (WeasyPrint 공식 문서 기반)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    libpq-dev \
    fonts-liberation \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 의존성 파일 먼저 복사하여 pip 캐시 활용
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 소스코드 복사
COPY . .

EXPOSE 8000

ENV PATH="/root/.local/bin:$PATH"

CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--preload", "main:app", "--bind", "0.0.0.0:8000"]
