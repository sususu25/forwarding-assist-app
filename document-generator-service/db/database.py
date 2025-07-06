import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# DB 접속 정보 환경 변수에서 읽기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 비밀번호에 특수문자가 있을 경우를 대비해 URL 인코딩
encoded_password = quote_plus(DB_PASSWORD)

# DB 접속 URL 구성: postgresql://username:password@host:port/dbname
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .models import Base

def init_db():
    inspector = inspect(engine)
    if not inspector.has_table("documents"):
        print("테이블이 존재하지 않아 새로 생성합니다...")
        Base.metadata.create_all(bind=engine)
    else:
        print("테이블이 이미 존재합니다.")

print("🧪 DATABASE_URL =", f"postgresql://{DB_USER}:********@{DB_HOST}:{DB_PORT}/{DB_NAME}")