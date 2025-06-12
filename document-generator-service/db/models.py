from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Document(Base):
    """PDF 생성 이력을 저장하는 테이블"""
    __tablename__ = "documents"          # ← 스키마 지정 필요 없음 (search_path = docsvc)

    id          = Column(Integer, primary_key=True, index=True)
    file_name   = Column(String,  nullable=False)
    doc_type    = Column(String,  nullable=False)
    exporter    = Column(String)
    destination = Column(String)
    created_at  = Column(DateTime, default=datetime.utcnow)
