from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from checker import check_for_violations
from schemas import CheckRequest

app = FastAPI()

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-errors")
def check(data: CheckRequest):
    return {"violations": check_for_violations(data)}
