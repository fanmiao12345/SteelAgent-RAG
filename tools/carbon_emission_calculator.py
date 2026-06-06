def calculate_carbon_emission(
    production_ton: float,
    emission_factor: float = 1.8,
) -> dict:
    total_emission = production_ton * emission_factor
    return {
        "production_ton": production_ton,
        "emission_factor": emission_factor,
        "total_emission_ton": round(total_emission, 2),
        "unit": "tCO2",
    }
