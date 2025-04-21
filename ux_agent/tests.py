from fastapi.testclient import TestClient
from fastapi import FastAPI
from ux_agent.api import ux_router
import pytest

app = FastAPI()
app.include_router(ux_router)

client = TestClient(app)

def test_ux_feedback_creation():
    response = client.post("/ux/create_feedback", json={
        "description": "Improve button accessibility",
        "assigned_to": "ux1",
        "context": {"component": "button"},
        "dependencies": [],
        "priority": 2
    })
    assert response.status_code == 201
    assert "feedback_id" in response.json()

def test_ux_feedback_status_not_found():
    response = client.get("/ux/status/notarealfeedbackid")
    assert response.status_code == 404

def test_conflict_resolution():
    feedback_a = {
        "id": "uxfb_a",
        "description": "A",
        "priority": 2,
        "timestamp": 1000
    }
    feedback_b = {
        "id": "uxfb_b",
        "description": "B",
        "priority": 1,
        "timestamp": 999
    }
    response = client.post("/ux/resolve_conflict", json={"feedback_a": feedback_a, "feedback_b": feedback_b})
    assert response.status_code == 200
    assert response.json()["resolved_feedback"]["id"] == "uxfb_a"
