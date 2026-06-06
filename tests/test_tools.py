import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.steel_weight_calculator import calculate_steel_weight
from tools.carbon_emission_calculator import calculate_carbon_emission
from tools.energy_cost_calculator import calculate_energy_cost
from tools.fault_diagnosis_tool import diagnose_fault
from tools.production_indicator_tool import calculate_indicators


def test_plate_weight():
    result = calculate_steel_weight("plate", thickness_mm=10, width_m=2, length_m=6)
    assert result["shape"] == "钢板"
    assert result["weight_kg"] == 942.0


def test_round_bar_weight():
    result = calculate_steel_weight("round_bar", diameter_mm=20, length_m=12)
    assert result["shape"] == "圆钢"
    assert result["weight_kg"] > 0


def test_carbon_emission():
    result = calculate_carbon_emission(1000, 1.8)
    assert result["total_emission_ton"] == 1800.0


def test_energy_cost():
    result = calculate_energy_cost(electricity_kwh=30000, electricity_price=0.65)
    assert result["electricity_cost"] == 19500.0
    assert result["total_cost"] == 19500.0


def test_energy_cost_with_gas():
    result = calculate_energy_cost(electricity_kwh=10000, electricity_price=0.65, gas_m3=500, gas_price=3.5)
    assert result["total_cost"] == 10000 * 0.65 + 500 * 3.5


def test_fault_diagnosis():
    result = diagnose_fault("连铸机", "结晶器液位波动")
    assert result["equipment"] == "连铸机"
    assert "拉速不稳定" in result["possible_causes"]


def test_production_indicators():
    result = calculate_indicators()
    assert result["total_records"] >= 10
    assert "qualified_rate" in result["indicators"][0]
