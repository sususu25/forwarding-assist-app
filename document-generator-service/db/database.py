import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# DB 접속 URL 구성: postgresql://username:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")
    #"postgresql://doc_user:docpass@localhost:5432/doc_service_db"

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

print("🧪 DATABASE_URL =", DATABASE_URL)