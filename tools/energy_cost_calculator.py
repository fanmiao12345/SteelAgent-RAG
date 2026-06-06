def calculate_energy_cost(
    electricity_kwh: float = 0,
    electricity_price: float = 0.65,
    gas_m3: float = 0,
    gas_price: float = 3.5,
) -> dict:
    electricity_cost = electricity_kwh * electricity_price
    gas_cost = gas_m3 * gas_price
    total_cost = electricity_cost + gas_cost
    return {
        "electricity_kwh": electricity_kwh,
        "electricity_price": electricity_price,
        "electricity_cost": round(electricity_cost, 2),
        "gas_m3": gas_m3,
        "gas_price": gas_price,
        "gas_cost": round(gas_cost, 2),
        "total_cost": round(total_cost, 2),
        "unit": "元",
    }
