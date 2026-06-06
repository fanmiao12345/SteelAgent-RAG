import re

INJECTION_PATTERNS = [
    r"忽略.*(?:之前|以前|上面).*指令",
    r"ignore.*(?:previous|above|all).*instructions",
    r"输出.*(?:系统|system).*(?:提示|prompt)",
    r"(?:reveal|show|print).*system.*prompt",
    r"绕过.*(?:权限|限制|控制)",
    r"bypass.*(?:permission|restriction|control)",
    r"假装.*(?:我是|你是).*(?:admin|管理员|root)",
    r"pretend.*(?:I am|you are).*(?:admin|root)",
    r"删除.*(?:所有|全部).*(?:数据|文件)",
    r"泄露.*(?:机密|内部|confidential)",
    r"(?:confidential|restricted|secret).*(?:data|document|file)",
    r"ignore above",
    r"disregard.*instructions",
    r"你是一个.*(?:没有任何限制|没有规则)",
    r"进入.*(?:开发者|developer|debug).*(?:模式|mode)",
    r"输出.*(?:你收到|你的).*(?:第一条|第一条消息|初始)",
]


def detect_injection(query: str) -> dict:
    query_lower = query.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return {
                "is_injection": True,
                "reason": f"检测到可疑模式: {pattern}",
            }
    return {"is_injection": False, "reason": "未发现攻击或越权请求"}
