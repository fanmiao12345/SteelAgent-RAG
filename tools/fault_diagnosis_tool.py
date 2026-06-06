FAULT_DATABASE = {
    "高炉": {
        "炉温异常": ["焦炭负荷变化", "风量波动", "喷煤量不稳定", "原料成分变化"],
        "煤气利用率下降": ["布料制度不合理", "风量不足", "焦炭质量下降", "炉况波动"],
        "炉墙结厚": ["炉温过高", "渣碱度异常", "冷却设备漏水", "布料偏析"],
        "悬料": ["风量过大", "炉料透气性差", "炉温过高", "炉型不规则"],
    },
    "转炉": {
        "终点碳高": ["供氧不足", "枪位过高", "造渣不良", "温度偏低"],
        "终点温度低": ["废钢加入过多", "供氧时间不足", "冷却剂过多"],
        "喷溅严重": ["枪位过低", "造渣不良", "炉型异常", "供氧强度过大"],
    },
    "连铸机": {
        "结晶器液位波动": ["拉速不稳定", "塞棒控制异常", "保护渣状态异常", "液位检测异常"],
        "铸坯表面裂纹": ["结晶器传热不均", "二冷水量不当", "拉速过快", "钢水温度偏高"],
        "漏钢": ["结晶器磨损", "保护渣性能差", "拉速过快", "铸坯凝固不良"],
    },
    "轧机": {
        "板形不良": ["轧辊磨损", "轧制力不均", "冷却水量不当", "张力控制异常"],
        "轧机振动": ["轧辊偏心", "轴承磨损", "齿轮间隙过大", "轧制速度共振"],
        "厚度偏差": ["AGC系统异常", "轧辊热凸度变化", "来料厚度波动", "轧制力波动"],
    },
}


def diagnose_fault(equipment: str, symptom: str) -> dict:
    for equip_name, symptoms in FAULT_DATABASE.items():
        if equip_name in equipment:
            for symptom_name, causes in symptoms.items():
                if symptom_name in symptom:
                    return {
                        "equipment": equip_name,
                        "symptom": symptom_name,
                        "possible_causes": causes,
                        "suggestion": f"建议依次排查以上可能原因，优先检查最常见因素。",
                    }
    return {
        "equipment": equipment,
        "symptom": symptom,
        "possible_causes": ["未找到匹配的故障数据库记录"],
        "suggestion": "请提供更详细的设备型号和故障现象，或联系设备工程师。",
    }
