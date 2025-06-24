FROM python:3.11-slim

WORKDIR /app

# 의존성 파일 먼저 복사하여 pip 캐시 활용
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 소스코드 복사
COPY . .

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"] 