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

    context = {
        "destination": data.destination,
        "packaging": data.packaging if hasattr(data, "packaging") else None,
        "items": data.items,
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
                violations.append(msg)
        except Exception as e:
            print(f"[WARN] 룰 평가 실패: {e} | rule_id={rule.get('id')} | cond={cond}")

    return violations
