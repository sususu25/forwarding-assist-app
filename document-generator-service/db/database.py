from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB 접속 URL 구성: postgresql://username:password@host:port/dbname
DATABASE_URL = "postgresql://doc_user:docpass@localhost:5432/doc_service_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .models import Base

def init_db():
    Base.metadata.create_all(bind=engine)