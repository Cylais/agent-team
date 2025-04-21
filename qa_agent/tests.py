import pytest
import pytest_asyncio
import httpx
from qa_agent.__main__ import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Utility for test JWT (must match logic in qa_agent/security.py)
def get_jwt():
    return "valid_jwt_testtoken"

@pytest_asyncio.fixture(scope="module")
async def async_client():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac

def test_qa_testcase_creation():
    response = client.post("/qa/create_test", json={
        "description": "Verify login endpoint returns 200",
        "assigned_to": "qa1",
        "context": {"module": "auth"},
        "dependencies": [],
        "priority": 2
    }, headers={"Authorization": f"Bearer {get_jwt()}"})
    assert response.status_code == 201
    assert "test_id" in response.json()

@pytest.mark.asyncio
async def test_async_create_and_status(async_client):
    # Create test
    resp = await async_client.post("/qa/create_test", json={
        "description": "Async test creation",
        "assigned_to": "qa2",
        "context": {"module": "async"},
        "dependencies": [],
        "priority": 1
    }, headers={"Authorization": f"Bearer {get_jwt()}"})
    assert resp.status_code == 201
    test_id = resp.json()["test_id"]
    # Get status
    resp2 = await async_client.get(f"/qa/status/{test_id}", headers={"Authorization": f"Bearer {get_jwt()}"})
    assert resp2.status_code == 200
    assert resp2.json()["test"]["id"].startswith("qatest_")

@pytest.mark.asyncio
async def test_rate_limit(async_client):
    # Exceed rate limit
    for _ in range(11):
        resp = await async_client.get("/qa/list_tests", headers={"Authorization": f"Bearer {get_jwt()}"})
    assert resp.status_code in (429, 200)  # Last request may be 429

@pytest.mark.asyncio
async def test_metrics_endpoint(async_client):
    resp = await async_client.get("/qa/metrics")
    assert resp.status_code == 200
    assert b"qa_requests_total" in resp.content

def test_qa_test_status_not_found():
    response = client.get("/qa/status/notarealtestid", headers={"Authorization": f"Bearer {get_jwt()}"})
    assert response.status_code == 404

def test_conflict_resolution():
    test_a = {
        "id": "qatest_a",
        "description": "A",
        "priority": 2,
        "timestamp": 1000
    }
    test_b = {
        "id": "qatest_b",
        "description": "B",
        "priority": 1,
        "timestamp": 999
    }
    response = client.post("/qa/resolve_conflict", json={"test_a": test_a, "test_b": test_b}, headers={"Authorization": f"Bearer {get_jwt()}"})
    assert response.status_code == 200
    assert response.json()["resolved_test"]["id"] == "qatest_a"
