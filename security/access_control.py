ROLE_PERMISSIONS = {
    "visitor": {
        "security_levels": ["public"],
        "tools": [],
        "description": "访客：只能查看公开行业知识",
    },
    "operator": {
        "security_levels": ["public", "internal"],
        "tools": ["steel_weight", "fault_diagnosis"],
        "description": "一线操作员：可查看操作规程、安全制度，使用基础工具",
    },
    "engineer": {
        "security_levels": ["public", "internal"],
        "tools": ["steel_weight", "fault_diagnosis", "carbon_emission", "energy_cost"],
        "description": "工程师：可查看工艺知识、设备故障、能耗碳排放",
    },
    "manager": {
        "security_levels": ["public", "internal", "confidential"],
        "tools": ["steel_weight", "carbon_emission", "energy_cost", "production_indicator"],
        "description": "管理人员：可查看生产指标、成本、能耗汇总",
    },
    "admin": {
        "security_levels": ["public", "internal", "confidential"],
        "tools": ["steel_weight", "carbon_emission", "energy_cost", "fault_diagnosis", "production_indicator"],
        "description": "管理员：全部权限",
    },
}

# 文档分类到角色的映射（用于 confidential 文档的细粒度控制）
CONFIDENTIAL_CATEGORY_MAP = {
    "process": ["engineer", "admin"],
    "equipment": ["engineer", "admin"],
    "statistics": ["manager", "admin"],
    "cost": ["manager", "admin"],
    "energy": ["manager", "admin"],
    "carbon": ["manager", "admin"],
}


def can_access_document(role: str, security_level: str, category: str = "") -> bool:
    if role not in ROLE_PERMISSIONS:
        return False
    if security_level == "confidential":
        if category:
            allowed_roles = CONFIDENTIAL_CATEGORY_MAP.get(category, ["admin"])
            return role in allowed_roles
        return "confidential" in ROLE_PERMISSIONS[role]["security_levels"]
    allowed_levels = ROLE_PERMISSIONS[role]["security_levels"]
    return security_level in allowed_levels


def can_use_tool(role: str, tool_name: str) -> bool:
    if role not in ROLE_PERMISSIONS:
        return False
    return tool_name in ROLE_PERMISSIONS[role]["tools"]


def get_role_info(role: str) -> dict:
    return ROLE_PERMISSIONS.get(role, {})
