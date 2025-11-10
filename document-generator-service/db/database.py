import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

# DB 접속 정보 환경 변수에서 DATABASE_URL 하나만 읽도록 수정
DATABASE_URL = os.getenv("DATABASE_URL")

# DATABASE_URL을 직접 create_engine에 전달합니다.
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

# 로그에는 비밀번호를 제외하고 출력합니다.
print("🧪 DB Connection Info =", DATABASE_URL)