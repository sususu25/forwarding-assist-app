from sqlalchemy.orm import Session
from .models import Document

# ----- Create ----------------------------------------------------
def create_document(db: Session, **kwargs) -> Document:
    doc = Document(**kwargs)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

# ----- Read ------------------------------------------------------
def list_documents(db: Session) -> list[Document]:
    return db.query(Document).order_by(Document.id.desc()).all()

def get_document(db: Session, doc_id: int) -> Document | None:
    return db.query(Document).filter(Document.id == doc_id).first()

# ----- Delete ----------------------------------------------------
def delete_document(db: Session, doc_id: int) -> bool:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False
