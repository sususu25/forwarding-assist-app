# mongo_seed.py
from pymongo import MongoClient
import json
from pathlib import Path
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["forwarding"]
collection = db["regulations"]

# 스크립트 파일의 위치를 기준으로 데이터 파일 경로를 정확히 찾습니다.
script_dir = Path(__file__).parent
info_json_path = script_dir / "data" / "info.json"

# 기존 규정 JSON 로딩
with open(info_json_path, "r", encoding="utf-8") as f:
    rules = json.load(f)

# 규정 삽입
for key, rule in rules.items():
    # 중복 방지 위해 country + cargo_type으로 덮어쓰기
    collection.replace_one(
        {"country": rule["country"], "cargo_type": rule["cargo_type"]},
        rule,
        upsert=True
    )

print("✅ 규정 데이터 MongoDB 삽입 완료")
