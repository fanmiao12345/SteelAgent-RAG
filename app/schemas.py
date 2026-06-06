from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str = "default"
    user_id: str = "anonymous"
    role: str = "visitor"
    query: str


class ChatResponse(BaseModel):
    answer: str
    query_type: str
    plan: list[str]
    citations: list[dict]
    used_tools: list[str]
    security: dict
    reflection: dict = {}


class SteelWeightRequest(BaseModel):
    shape: str
    thickness_mm: float = 0
    width_m: float = 0
    length_m: float = 0
    diameter_mm: float = 0
    outer_diameter_mm: float = 0
    inner_diameter_mm: float = 0


class CarbonEmissionRequest(BaseModel):
    production_ton: float
    emission_factor: float = 1.8


class EnergyCostRequest(BaseModel):
    electricity_kwh: float = 0
    electricity_price: float = 0.65
    gas_m3: float = 0
    gas_price: float = 3.5


class FaultDiagnosisRequest(BaseModel):
    equipment: str
    symptom: str


class ProductionIndicatorRequest(BaseModel):
    csv_path: str = "data/production/production_sample.csv"
