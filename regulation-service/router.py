# regulation-service/router.py
from fastapi import APIRouter, Query
from schema import RegulationResponse
from pymongo import MongoClient
from pathlib import Path
import json
import os

router = APIRouter()

# ──────────────────────────────────
#  MongoDB 연결  (forwarding DB)
# ──────────────────────────────────
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["forwarding"]
collection = db["regulations"]           # RegulationInfo 저장 컬렉션

# ──────────────────────────────────
#  1) 규정 상세 조회  →  GET /info
# ──────────────────────────────────
@router.get("/info", response_model=RegulationResponse)
def get_regulation_info(
        country: str = Query(..., description="수입(출)국가"),
        cargo_type: str = Query(..., description="화물 유형")
):
    """
    ① country + cargo_type 정확 매칭
    ② country='common' + cargo_type 보정
    ③ 둘 다 없으면 기본 메시지
    """
    rule = collection.find_one({"country": country, "cargo_type": cargo_type})

    if not rule:
        rule = collection.find_one({"country": "common", "cargo_type": cargo_type})

    if not rule:
        return {
            "country": country,
            "cargo_type": cargo_type,
            "required_documents": [],
            "packaging_requirement": None,
            "co_required": None,
            "notes": "해당 조건에 대한 규정 정보가 없습니다."
        }

    rule.pop("_id", None)        # ObjectId 제거
    return rule


# ──────────────────────────────────
#  2) 룰 전체 반환  →  GET /rules
# ──────────────────────────────────
@router.get("/rules")
def get_all_rules():
    """
    error-check-service 캐싱 용도.
    rules.json 이 없으면 빈 리스트 반환.
    """
    rules_path = Path(__file__).parent / "data" / "rules.json"
    try:
        with open(rules_path, "r", encoding="utf-8") as fp:
            rules = json.load(fp)
        return {"rules": rules}
    except FileNotFoundError:
        return {"rules": [], "error": "rules.json 파일이 존재하지 않습니다."}

