from schemas import CheckRequest
from cache import get_rules

def check_for_violations(data: CheckRequest):
    """
    info.json 의 각 rule = {"condition": "...", "message": "..."}
    condition 문자열은 안전상의 이유로 DSL/파서로 교체 권장.
    현재는 eval 사용 (빠른 프로토타입).
    """
    rules = get_rules()
    violations = []

    # items 리스트의 각 Pydantic 모델을 dict로 변환
    items_as_dicts = [item.dict() for item in data.items]

    context = {
        "data": data,  # data 객체 자체를 컨텍스트에 추가
        "destination": data.destination,
        "packaging": data.packaging if hasattr(data, "packaging") else None,
        "items": items_as_dicts, # dict로 변환된 리스트 사용
        "any": any,
        "all": all,
        "sum": sum,
    }

    for rule in rules:
        cond = rule.get("condition", "")
        msg = rule.get("message", "규정 위반")

        try:
            result = eval(cond, {}, context)
            print(f"[DEBUG] rule_id={rule.get('id')} → {result} | cond={cond}")
            if cond and result:
                violation = {"id": rule.get("id"), "message": msg}
                # --- custom details extraction for better UX ---
                if rule.get("id") == "USA_LITHIUM_BAN":
                    violation["items"] = [it["name"] for it in items_as_dicts if "lithium" in it.get("name", "").lower()]
                elif rule.get("id") == "USA_LITHIUM_PACKAGING":
                    violation["items"] = [it["name"] for it in items_as_dicts if "lithium" in it.get("name", "").lower()]
                    violation["packaging"] = True # packaging 필드 하이라이트용
                elif rule.get("id") == "WOOD_PACKAGING":
                    violation["packaging"] = data.packaging if hasattr(data, "packaging") else None
                elif rule.get("id") == "HEAVY_CARGO_CHINA":
                    violation["total_weight"] = sum(it.get("weight", 0) for it in items_as_dicts)
                violations.append(violation)
        except Exception as e:
            print(f"[WARN] 룰 평가 실패: {e} | rule_id={rule.get('id')} | cond={cond}")

    return violations
