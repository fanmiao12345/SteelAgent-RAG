import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.access_control import can_access_document, can_use_tool


def test_visitor_can_access_public():
    assert can_access_document("visitor", "public") is True


def test_visitor_cannot_access_internal():
    assert can_access_document("visitor", "internal") is False


def test_visitor_cannot_access_confidential():
    assert can_access_document("visitor", "confidential") is False


def test_operator_can_access_public_internal():
    assert can_access_document("operator", "public") is True
    assert can_access_document("operator", "internal") is True


def test_operator_cannot_access_confidential():
    assert can_access_document("operator", "confidential") is False


def test_engineer_can_access_process_confidential():
    assert can_access_document("engineer", "confidential", "process") is True
    assert can_access_document("engineer", "confidential", "equipment") is True


def test_engineer_cannot_access_cost_confidential():
    assert can_access_document("engineer", "confidential", "cost") is False


def test_manager_can_access_statistics_confidential():
    assert can_access_document("manager", "confidential", "statistics") is True
    assert can_access_document("manager", "confidential", "cost") is True
    assert can_access_document("manager", "confidential", "energy") is True


def test_manager_cannot_access_process_confidential():
    assert can_access_document("manager", "confidential", "process") is False


def test_admin_can_access_all():
    assert can_access_document("admin", "public") is True
    assert can_access_document("admin", "internal") is True
    assert can_access_document("admin", "confidential", "process") is True
    assert can_access_document("admin", "confidential", "cost") is True


def test_visitor_cannot_use_tools():
    assert can_use_tool("visitor", "steel_weight") is False


def test_operator_can_use_basic_tools():
    assert can_use_tool("operator", "steel_weight") is True
    assert can_use_tool("operator", "fault_diagnosis") is True


def test_operator_cannot_use_advanced_tools():
    assert can_use_tool("operator", "carbon_emission") is False
    assert can_use_tool("operator", "production_indicator") is False
