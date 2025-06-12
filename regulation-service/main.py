from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ 추가됨
from router import router

app = FastAPI(title="Regulation Service")

# ✅ CORS 설정 추가됨 (React 요청 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 포함
app.include_router(router)

# 헬스 체크용 엔드포인트
@app.get("/")
def health_check():
    return {"status": "regulation-service running"}

@app.get("/regulations")
def get_regulations(country: str, cargo_type: str):
    # 예시 리턴
    return {
        "country": country,
        "cargo_type": cargo_type,
        "required_documents": ["Invoice", "Packing List"],
        "packaging_requirement": "Pallet",
        "co_required": True,
        "notes": "Handle with care"
    }

