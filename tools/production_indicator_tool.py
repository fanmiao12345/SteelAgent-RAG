import os
import pandas as pd


def load_production_data(csv_path: str = "data/production/production_sample.csv") -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"生产数据文件不存在: {csv_path}")
    return pd.read_csv(csv_path)


def calculate_indicators(csv_path: str = "data/production/production_sample.csv") -> dict:
    df = load_production_data(csv_path)
    results = []
    for _, row in df.iterrows():
        qualified_rate = row["qualified_ton"] / row["production_ton"] * 100 if row["production_ton"] > 0 else 0
        unit_electricity = row["electricity_kwh"] / row["production_ton"] if row["production_ton"] > 0 else 0
        unit_cost = row["total_cost"] / row["production_ton"] if row["production_ton"] > 0 else 0
        carbon_intensity = row["carbon_emission_ton"] / row["production_ton"] if row["production_ton"] > 0 else 0
        results.append({
            "date": row["date"],
            "line_name": row["line_name"],
            "product_type": row["product_type"],
            "production_ton": row["production_ton"],
            "qualified_rate": round(qualified_rate, 2),
            "unit_electricity_kwh": round(unit_electricity, 2),
            "unit_cost": round(unit_cost, 2),
            "carbon_intensity": round(carbon_intensity, 4),
        })
    return {"indicators": results, "total_records": len(results)}
