def reflect_answer(answer: str, citations: list[dict], query: str) -> dict:
    issues = []

    if not answer or len(answer.strip()) < 10:
        issues.append("回答内容过短或为空")

    if not citations:
        issues.append("回答缺少引用来源")

    if "我不确定" in answer or "无法回答" in answer:
        issues.append("回答表达了不确定性")

    return {
        "passed": len(issues) == 0,
        "issues": issues,
    }
