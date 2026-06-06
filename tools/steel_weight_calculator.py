DENSITY = 7850  # kg/m³


def calculate_steel_weight(
    shape: str,
    thickness_mm: float = 0,
    width_m: float = 0,
    length_m: float = 0,
    diameter_mm: float = 0,
    outer_diameter_mm: float = 0,
    inner_diameter_mm: float = 0,
) -> dict:
    if shape == "plate":
        volume_m3 = (thickness_mm / 1000) * width_m * length_m
        weight_kg = volume_m3 * DENSITY
        return {
            "shape": "钢板",
            "volume_m3": round(volume_m3, 4),
            "weight_kg": round(weight_kg, 2),
            "weight_ton": round(weight_kg / 1000, 4),
        }
    elif shape == "round_bar":
        radius_m = (diameter_mm / 1000) / 2
        import math
        volume_m3 = math.pi * radius_m**2 * length_m
        weight_kg = volume_m3 * DENSITY
        return {
            "shape": "圆钢",
            "volume_m3": round(volume_m3, 4),
            "weight_kg": round(weight_kg, 2),
            "weight_ton": round(weight_kg / 1000, 4),
        }
    elif shape == "pipe":
        import math
        outer_r = (outer_diameter_mm / 1000) / 2
        inner_r = (inner_diameter_mm / 1000) / 2
        volume_m3 = math.pi * (outer_r**2 - inner_r**2) * length_m
        weight_kg = volume_m3 * DENSITY
        return {
            "shape": "钢管",
            "volume_m3": round(volume_m3, 4),
            "weight_kg": round(weight_kg, 2),
            "weight_ton": round(weight_kg / 1000, 4),
        }
    elif shape == "rebar":
        import math
        radius_m = (diameter_mm / 1000) / 2
        volume_m3 = math.pi * radius_m**2 * length_m
        weight_kg = volume_m3 * DENSITY
        return {
            "shape": "螺纹钢",
            "volume_m3": round(volume_m3, 4),
            "weight_kg": round(weight_kg, 2),
            "weight_ton": round(weight_kg / 1000, 4),
        }
    else:
        return {"error": f"不支持的钢材类型: {shape}，支持: plate, round_bar, pipe, rebar"}
