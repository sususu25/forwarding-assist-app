from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware           # <<< CORS
from pathlib import Path

from db.database import SessionLocal, init_db
from db import crud
from schemas import PdfRequest
from utils.pdf_creator import generate_pdf

# ────────────────────────────────────────────────
# FastAPI APP & CORS 설정
# ────────────────────────────────────────────────
app = FastAPI()
app.add_middleware(                                        # <<< CORS 미들웨어
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프런트 포트
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()

# ────────────────────────────────────────────────
# 1) PDF 생성 → DB 기록
# ────────────────────────────────────────────────
@app.post("/generate-pdf", response_model=dict)
async def create_pdf(payload: PdfRequest = Body(...)):
    file_path = generate_pdf(payload.dict())

    db = SessionLocal()
    doc = crud.create_document(
        db,
        file_name=Path(file_path).name,
        doc_type="Packing List",
        exporter=payload.exporter,
        destination=payload.destination,
    )
    db.close()
    return {"id": doc.id, "file_name": doc.file_name}

# ────────────────────────────────────────────────
# 2) 문서 리스트
# ────────────────────────────────────────────────
@app.get("/documents")
def list_docs():
    db = SessionLocal()
    docs = crud.list_documents(db)
    db.close()
    return docs

# ────────────────────────────────────────────────
# 3) 단건 조회 + PDF 다운로드
# ────────────────────────────────────────────────
@app.get("/documents/{doc_id}")
def download_doc(doc_id: int):
    db = SessionLocal()
    doc = crud.get_document(db, doc_id)
    db.close()

    if not doc:
        raise HTTPException(404, "Document not found")

    file_path = Path("output") / doc.file_name
    if not file_path.exists():
        raise HTTPException(404, "File missing on disk")

    return FileResponse(file_path, media_type="application/pdf", filename=doc.file_name)

# ────────────────────────────────────────────────
# 4) 삭제
# ────────────────────────────────────────────────
@app.delete("/documents/{doc_id}")
def delete_doc(doc_id: int):
    db = SessionLocal()
    result = crud.delete_document(db, doc_id)
    db.close()
    if not result:
        raise HTTPException(404, "Document not found")
    return {"deleted": doc_id}

# ────────────────────────────────────────────────
# 5) 헬스 체크
# ────────────────────────────────────────────────
@app.get("/ping")
def ping():
    return {"pong": True}
