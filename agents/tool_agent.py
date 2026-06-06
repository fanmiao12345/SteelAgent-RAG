import re
from security.access_control import can_use_tool
from tools.steel_weight_calculator import calculate_steel_weight
from tools.carbon_emission_calculator import calculate_carbon_emission
from tools.energy_cost_calculator import calculate_energy_cost
from tools.fault_diagnosis_tool import diagnose_fault
from tools.production_indicator_tool import calculate_indicators


def detect_and_run_tool(query: str, role: str) -> dict | None:
    query_lower = query.lower()

    # 钢材重量计算
    weight_match = re.search(r"(?:厚度|直径)\s*(\d+)\s*mm.*?(?:宽度|长度)\s*(\d+)", query)
    if any(kw in query_lower for kw in ["钢板重量", "圆钢重量", "钢管重量", "螺纹钢重量", "钢材重量"]):
        if not can_use_tool(role, "steel_weight"):
            return {"error": "您没有钢材重量计算工具的使用权限"}
        numbers = re.findall(r"(\d+(?:\.\d+)?)", query)
        if "钢板" in query and len(numbers) >= 3:
            return calculate_steel_weight("plate", thickness_mm=float(numbers[0]), width_m=float(numbers[1]), length_m=float(numbers[2]))
        elif "圆钢" in query and len(numbers) >= 2:
            return calculate_steel_weight("round_bar", diameter_mm=float(numbers[0]), length_m=float(numbers[1]))
        elif "螺纹钢" in query and len(numbers) >= 2:
            return calculate_steel_weight("rebar", diameter_mm=float(numbers[0]), length_m=float(numbers[1]))

    # 碳排放计算
    if "碳排放" in query_lower and any(kw in query_lower for kw in ["计算", "多少", "产量"]):
        if not can_use_tool(role, "carbon_emission"):
            return {"error": "您没有碳排放计算工具的使用权限"}
        numbers = re.findall(r"(\d+(?:\.\d+)?)", query)
        if len(numbers) >= 1:
            factor = float(numbers[1]) if len(numbers) >= 2 else 1.8
            return calculate_carbon_emission(float(numbers[0]), factor)

    # 能耗成本计算
    if any(kw in query_lower for kw in ["用电", "电费", "能耗成本", "电价"]):
        if not can_use_tool(role, "energy_cost"):
            return {"error": "您没有能耗成本计算工具的使用权限"}
        numbers = re.findall(r"(\d+(?:\.\d+)?)", query)
        if len(numbers) >= 1:
            kwh = float(numbers[0])
            price = float(numbers[1]) if len(numbers) >= 2 else 0.65
            return calculate_energy_cost(electricity_kwh=kwh, electricity_price=price)

    # 故障诊断
    if any(kw in query_lower for kw in ["故障", "异常", "原因"]):
        if not can_use_tool(role, "fault_diagnosis"):
            return {"error": "您没有故障诊断工具的使用权限"}
        equipment = ""
        symptom = ""
        for equip in ["高炉", "转炉", "连铸机", "轧机"]:
            if equip in query:
                equipment = equip
                break
        for s in ["液位波动", "表面裂纹", "振动", "板形不良", "炉温异常", "煤气利用率下降"]:
            if s in query:
                symptom = s
                break
        if equipment and symptom:
            return diagnose_fault(equipment, symptom)

    # 生产指标
    if any(kw in query_lower for kw in ["合格率", "产量", "生产数据", "指标"]):
        if not can_use_tool(role, "production_indicator"):
            return {"error": "您没有生产指标工具的使用权限"}
        try:
            return calculate_indicators()
        except Exception as e:
            return {"error": str(e)}

    return None
