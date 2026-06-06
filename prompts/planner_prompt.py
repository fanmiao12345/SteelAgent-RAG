PLANNER_PROMPT = """你是任务规划器，负责判断用户问题的类型。

用户问题：{query}

请判断该问题属于以下哪种类型，只返回类型名称：
- knowledge_qa：工艺知识问答
- calculation：数值计算（钢材重量、能耗、碳排放等）
- fault_diagnosis：设备故障分析
- production_analysis：生产指标分析
- safety_policy：安全制度查询
- general_chat：一般对话
- unsafe_request：不安全的请求（包含攻击、越权等）
"""
