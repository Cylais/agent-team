import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import FastAPI
from pm_agent.api import pm_router
from pm_agent.core import PMStateManager
import asyncio
import os

# --- JWT token stub for tests ---
TEST_JWT = "Bearer test.jwt.token"

def auth_headers():
    return {"Authorization": TEST_JWT}

@pytest_asyncio.fixture
async def async_client():
    app = FastAPI()
    app.include_router(pm_router)
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.mark.asyncio
async def test_task_assignment(async_client):
    response = await async_client.post("/pm/assign_task", json={
        "objective": "Implement auth",
        "context": {"priority": "high"},
        "dependencies": [],
        "assigned_to": None,
        "priority": 2
    }, headers=auth_headers())
    assert response.status_code == 201
    assert "task_id" in response.json()

@pytest.mark.asyncio
async def test_task_status_not_found(async_client):
    response = await async_client.get("/pm/status/notarealtaskid", headers=auth_headers())
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_conflict_resolution(async_client):
    task_a = {
        "id": "task_a",
        "objective": "A",
        "priority": 2,
        "timestamp": 1000
    }
    task_b = {
        "id": "task_b",
        "objective": "B",
        "priority": 1,
        "timestamp": 999
    }
    response = await async_client.post("/pm/resolve_conflict", json={"task_a": task_a, "task_b": task_b}, headers=auth_headers())
    assert response.status_code == 200
    assert response.json()["resolved_task"]["id"] == "task_a"

@pytest.mark.asyncio
async def test_metrics_endpoint(async_client):
    response = await async_client.get("/pm/metrics")
    assert response.status_code == 200
    assert b"pm_task_create_total" in response.content

@pytest.mark.asyncio
async def test_circuit_breaker_triggers(monkeypatch, async_client):
    # Simulate Redis failure by monkeypatching PMStateManager async_create_task
    async def fail_create_task(*args, **kwargs):
        raise Exception("Redis down")
    monkeypatch.setattr(PMStateManager, "async_create_task", fail_create_task)
    response = await async_client.post("/pm/assign_task", json={
        "objective": "CB test",
        "context": {},
        "dependencies": [],
        "assigned_to": None,
        "priority": 1
    }, headers=auth_headers())
    assert response.status_code == 500 or response.status_code == 422

@pytest.mark.asyncio
async def test_tracing_headers_propagation(async_client):
    # Just ensure tracing headers are accepted and do not break API
    trace_headers = {"traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"}
    trace_headers.update(auth_headers())
    response = await async_client.post("/pm/assign_task", json={
        "objective": "Trace test",
        "context": {},
        "dependencies": [],
        "assigned_to": None,
        "priority": 1
    }, headers=trace_headers)
    assert response.status_code == 201

# --- Legacy sync tests below (to be removed after migration) ---
# def test_task_assignment(): ...
# def test_task_status_not_found(): ...
# def test_conflict_resolution(): ...
