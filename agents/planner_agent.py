import re
from llm_client import llm_client
from prompts.planner_prompt import PLANNER_PROMPT


def classify_query(query: str) -> str:
    query_lower = query.lower()

    # 先用规则快速判断
    calc_keywords = ["重量", "计算", "多少吨", "多少千克", "碳排放", "能耗", "成本", "电价"]
    if any(kw in query_lower for kw in calc_keywords):
        return "calculation"

    fault_keywords = ["故障", "异常", "原因", "振动", "泄漏", "报警", "液位波动"]
    if any(kw in query_lower for kw in fault_keywords):
        return "fault_diagnosis"

    safety_keywords = ["安全", "制度", "规程", "作业要求", "防护"]
    if any(kw in query_lower for kw in safety_keywords):
        return "safety_policy"

    production_keywords = ["合格率", "产量", "生产数据", "指标", "统计"]
    if any(kw in query_lower for kw in production_keywords):
        return "production_analysis"

    # 尝试用 LLM 分类
    try:
        prompt = PLANNER_PROMPT.format(query=query)
        result = llm_client.chat(
            llm_client.build_messages("你是任务分类器。", prompt),
            temperature=0.1,
        )
        result = result.strip().lower()
        valid_types = ["knowledge_qa", "calculation", "fault_diagnosis",
                       "production_analysis", "safety_policy", "general_chat", "unsafe_request"]
        for t in valid_types:
            if t in result:
                return t
    except Exception:
        pass

    return "knowledge_qa"
