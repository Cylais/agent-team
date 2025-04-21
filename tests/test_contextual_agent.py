import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure 'app' is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.contextual_agent import app

client = TestClient(app)

def test_admin_after_hours():
    payload = {
        "user_role": "admin",
        "time_of_day": "after_hours",
        "agent_state": "busy",
        "data": {}
    }
    response = client.post("/agent/contextual_decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "full_access"
    assert data["context_used"]["user_role"] == "admin"
    assert data["note"] == "Limited support after hours."

def test_observer_working_hours():
    payload = {
        "user_role": "observer",
        "time_of_day": "working_hours",
        "agent_state": "idle",
        "data": {}
    }
    response = client.post("/agent/contextual_decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "read_only"
    assert "note" not in data

def test_error_state():
    payload = {
        "user_role": "admin",
        "time_of_day": "working_hours",
        "agent_state": "error",
        "data": {}
    }
    response = client.post("/agent/contextual_decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "degraded_mode"
    assert data["context_used"]["agent_state"] == "error"

def test_field_masking_decision_only():
    payload = {
        "user_role": "admin",
        "time_of_day": "working_hours",
        "agent_state": "idle",
        "data": {}
    }
    response = client.post("/agent/contextual_decision?fields=decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data == {"decision": "full_access"}

def test_field_masking_note_only():
    payload = {
        "user_role": "observer",
        "time_of_day": "after_hours",
        "agent_state": "idle",
        "data": {}
    }
    response = client.post("/agent/contextual_decision?fields=note", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data == {"note": "Limited support after hours."}

def test_field_masking_invalid_field():
    payload = {
        "user_role": "observer",
        "time_of_day": "working_hours",
        "agent_state": "idle",
        "data": {}
    }
    response = client.post("/agent/contextual_decision?fields=notarealfield", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "No valid fields requested"

def test_missing_required_field():
    payload = {
        # 'user_role' missing
        "time_of_day": "working_hours",
        "agent_state": "idle",
        "data": {}
    }
    response = client.post("/agent/contextual_decision", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data or "detail" in data

def test_extra_field():
    payload = {
        "user_role": "admin",
        "time_of_day": "working_hours",
        "agent_state": "idle",
        "data": {},
        "extra": "surplus"
    }
    response = client.post("/agent/contextual_decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "full_access"

def test_malformed_json():
    bad_json = '{"user_role": "admin", "time_of_day": "working_hours", "agent_state": "idle", "data": '  # Truncated
    response = client.post("/agent/contextual_decision", data=bad_json, headers={"Content-Type": "application/json"})
    assert response.status_code in (400, 422)
    data = response.json()
    assert "error" in data or "detail" in data

def test_unicode_and_large_payload():
    payload = {
        "user_role": "админ",  # Cyrillic for 'admin'
        "time_of_day": "рабочее_время",  # 'working_hours' in Russian
        "agent_state": "idle",
        "data": {"text": "𝄞" * 10000}  # Large unicode payload
    }
    response = client.post("/agent/contextual_decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "decision" in data
