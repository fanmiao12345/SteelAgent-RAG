import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["project"] == "SteelAgent-RAG"


def test_roles():
    resp = client.get("/roles")
    assert resp.status_code == 200
    data = resp.json()
    assert "visitor" in data
    assert "admin" in data


def test_chat_basic():
    resp = client.post("/chat", json={
        "session_id": "test001",
        "user_id": "u001",
        "role": "engineer",
        "query": "高炉炼铁的主要流程是什么？",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "query_type" in data
    assert "security" in data


def test_tool_fault_diagnosis_api():
    resp = client.post("/tool/fault-diagnosis", json={
        "equipment": "连铸机",
        "symptom": "结晶器液位波动",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["equipment"] == "连铸机"
    assert "液位检测异常" in data["possible_causes"]


def test_tool_production_indicator_api():
    resp = client.post("/tool/production-indicator", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_records"] >= 10
