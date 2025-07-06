import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

# DB 접속 정보 환경 변수에서 읽기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# DATABASE_URL을 직접 조립하는 대신, SQLAlchemy에 연결 정보를 직접 전달합니다.
# 이 방법이 특수문자를 포함한 비밀번호를 가장 안전하게 처리합니다.
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(db_url)
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
print("🧪 DB Connection Info =", f"postgresql://{DB_USER}:********@{DB_HOST}:{DB_PORT}/{DB_NAME}")