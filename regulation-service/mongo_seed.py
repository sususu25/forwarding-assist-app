# mongo_seed.py
from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017")  # 로컬 MongoDB
db = client["forwarding"]
collection = db["regulations"]

# 기존 규정 JSON 로딩
with open("data/info.json", "r", encoding="utf-8") as f:
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
