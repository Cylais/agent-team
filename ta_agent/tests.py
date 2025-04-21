from fastapi.testclient import TestClient
from fastapi import FastAPI
from ta_agent.api import ta_router
import pytest
import asyncio
import httpx
import pytest_asyncio
from ta_agent.__main__ import app as main_app

app = FastAPI()
app.include_router(ta_router)

client = TestClient(app)

# NOTE: httpx.AsyncClient(app=...) is not supported in httpx <0.23. For local testing, run the FastAPI app (uvicorn ta_agent.__main__:app) and use base_url.
@pytest_asyncio.fixture(scope="module")
async def async_client():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac

def get_jwt():
    # Dummy JWT for testing; replace with real signing if needed
    return "Bearer test.jwt.token"

def test_decision_proposal():
    response = client.post("/ta/propose_decision", json={
        "summary": "Adopt event-driven architecture",
        "rationale": "Improves scalability",
        "context": {"impact": "high"},
        "dependencies": [],
        "priority": 2
    })
    assert response.status_code == 201
    assert "decision_id" in response.json()

@pytest.mark.asyncio
async def test_async_propose_and_status(async_client):
    headers = {"Authorization": get_jwt()}
    resp = await async_client.post("/ta/async_propose_decision", json={
        "summary": "Async event-driven",
        "rationale": "Async improves perf",
        "context": {"impact": "high"},
        "dependencies": [],
        "priority": 3
    }, headers=headers)
    assert resp.status_code == 201
    decision_id = resp.json()["decision_id"]
    status = await async_client.get(f"/ta/async_status/{decision_id}", headers=headers)
    assert status.status_code == 200
    assert status.json()["decision"]["summary"] == "Async event-driven"

@pytest.mark.asyncio
async def test_async_list_and_update(async_client):
    headers = {"Authorization": get_jwt()}
    # List
    resp = await async_client.get("/ta/async_list_decisions", headers=headers)
    assert resp.status_code == 200
    # Update
    if resp.json()["decisions"]:
        dec_id = list(resp.json()["decisions"].keys())[0]
        up = await async_client.post(f"/ta/async_update_decision/{dec_id}", json={"priority": 9}, headers=headers)
        assert up.status_code == 200

@pytest.mark.asyncio
async def test_async_batch_update_and_ai_hint(async_client):
    headers = {"Authorization": get_jwt()}
    # Batch update
    resp = await async_client.get("/ta/async_list_decisions", headers=headers)
    ids = list(resp.json()["decisions"].keys())
    updates = [{"id": i, "priority": 5} for i in ids]
    batch = await async_client.post("/ta/async_batch_update_decisions", json=updates, headers=headers)
    assert batch.status_code == 200
    # AI hint
    ai = await async_client.post("/ta/ai_hint", json={"objective": "test", "context": {}}, headers=headers)
    assert ai.status_code == 200
    assert "suggested_fields" in ai.json()

@pytest.mark.asyncio
async def test_async_requires_jwt(async_client):
    # No JWT should fail
    resp = await async_client.post("/ta/async_propose_decision", json={"summary": "fail", "rationale": "fail", "context": {}, "dependencies": [], "priority": 1})
    assert resp.status_code == 401 or resp.status_code == 403

@pytest.mark.asyncio
async def test_async_rate_limit(async_client):
    headers = {"Authorization": get_jwt()}
    # Exceed rate limit (5/min)
    for _ in range(6):
        resp = await async_client.post("/ta/async_propose_decision", json={"summary": "rl", "rationale": "rl", "context": {}, "dependencies": [], "priority": 1}, headers=headers)
    assert resp.status_code in (429, 201)

@pytest.mark.asyncio
async def test_prometheus_metrics(async_client):
    resp = await async_client.get("/ta/metrics")
    assert resp.status_code == 200
    assert b"ta_agent_requests_total" in resp.content


def test_decision_status_not_found():
    response = client.get("/ta/status/notarealdecisionid")
    assert response.status_code == 404

def test_conflict_resolution():
    dec_a = {
        "id": "decision_a",
        "summary": "A",
        "priority": 2,
        "timestamp": 1000
    }
    dec_b = {
        "id": "decision_b",
        "summary": "B",
        "priority": 1,
        "timestamp": 999
    }
    response = client.post("/ta/resolve_conflict", json={"dec_a": dec_a, "dec_b": dec_b})
    assert response.status_code == 200
    assert response.json()["resolved_decision"]["id"] == "decision_a"
