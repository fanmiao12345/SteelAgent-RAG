from security.injection_detector import detect_injection


SENSITIVE_KEYWORDS = ["confidential", "restricted", "机密", "保密", "内部数据", "内部文档", "全部文档"]


def check_security(query: str, role: str = "visitor") -> dict:
    result = detect_injection(query)
    if result["is_injection"]:
        return {
            "decision": "deny",
            "reason": result["reason"],
        }
    if role in {"visitor", "operator"} and any(kw in query.lower() for kw in SENSITIVE_KEYWORDS):
        return {
            "decision": "degrade",
            "reason": "检测到可能涉及越权内容，将只基于当前角色允许访问的资料回答",
        }
    return {
        "decision": "allow",
        "reason": "未发现攻击或越权请求",
    }
