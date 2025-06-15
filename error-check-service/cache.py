import requests
import time
import os

RULES_URL = os.getenv("RULES_URL", "http://localhost:8001/rules")
CACHE_TTL = 3600  # 1시간

_cache = {"data": None, "ts": 0}

def get_rules():
    """규정 룰을 TTL 캐시로 유지"""
    now = time.time()

    # 캐시 hit
    if _cache["data"] and (now - _cache["ts"] < CACHE_TTL):
        return _cache["data"]

    # 캐시 miss → 원격 호출
    try:
        res = requests.get(RULES_URL, timeout=3)
        res.raise_for_status()
        rules = res.json().get("rules", [])
        _cache["data"], _cache["ts"] = rules, now
        return rules
    except Exception as e:
        # 실패 시 마지막 캐시라도 반환
        print(f"[ERROR] 규정 룰 갱신 실패: {e}")
        return _cache["data"] or []
