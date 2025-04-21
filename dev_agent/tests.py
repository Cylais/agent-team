import os
import pytest
import jwt
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch
from dev_agent.api import dev_router
from dev_agent.core import DevTask

SECRET_KEY = os.getenv("DEV_AGENT_JWT_SECRET", "dev-secret-key")

import pytest_asyncio

@pytest_asyncio.fixture
async def async_client():
    app = FastAPI()
    app.include_router(dev_router)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def jwt_token():
    payload = {"sub": "testuser", "exp": 9999999999}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.mark.asyncio
@patch("dev_agent.core.redis.from_url", new_callable=AsyncMock)
async def test_dev_task_creation(mock_redis, async_client, jwt_token):
    redis_mock = AsyncMock()
    redis_mock.hset.return_value = True
    redis_mock.hget.return_value = None
    redis_mock.hkeys.return_value = []
    mock_redis.return_value = redis_mock
    response = await async_client.post(
        "/dev/create_task",
        json={
            "description": "Implement login endpoint",
            "assigned_to": "dev1",
            "context": {"module": "auth"},
            "dependencies": [],
            "priority": 2
        },
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 201
    assert "task_id" in response.json()

@pytest.mark.asyncio
@patch("dev_agent.core.redis.from_url", new_callable=AsyncMock)
async def test_dev_task_status_not_found(mock_redis, async_client, jwt_token):
    redis_mock = AsyncMock()
    redis_mock.hget.return_value = None
    mock_redis.return_value = redis_mock
    response = await async_client.get(
        "/dev/status/notarealtaskid",
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 404

@pytest.mark.asyncio
@patch("dev_agent.core.redis.from_url", new_callable=AsyncMock)
async def test_conflict_resolution(mock_redis, async_client, jwt_token):
    redis_mock = AsyncMock()
    mock_redis.return_value = redis_mock
    task_a = {
        "id": "devtask_a",
        "description": "A",
        "priority": 2,
        "timestamp": 1000,
        "status": "pending",
        "dependencies": []
    }
    task_b = {
        "id": "devtask_b",
        "description": "B",
        "priority": 1,
        "timestamp": 999,
        "status": "pending",
        "dependencies": []
    }
    response = await async_client.post(
        "/dev/resolve_conflict",
        json={"task_a": task_a, "task_b": task_b},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 200
    assert response.json()["resolved_task"]["id"] == "devtask_a"

@pytest.mark.asyncio
@patch("dev_agent.core.redis.from_url", new_callable=AsyncMock)
@pytest.mark.parametrize("task_a,task_b,expected", [
    ({"priority": 1, "timestamp": 100, "status": "pending", "dependencies": []}, {"priority": 2, "timestamp": 200, "status": "pending", "dependencies": []}, "task_b"),
    ({"priority": 2, "timestamp": 200, "status": "pending", "dependencies": []}, {"priority": 1, "timestamp": 100, "status": "pending", "dependencies": []}, "task_a"),
    ({"priority": 1, "timestamp": 100, "status": "completed", "dependencies": []}, {"priority": 2, "timestamp": 200, "status": "pending", "dependencies": []}, "task_a"),
])
async def test_conflict_resolution_param(mock_redis, async_client, jwt_token, task_a, task_b, expected):
    redis_mock = AsyncMock()
    mock_redis.return_value = redis_mock
    task_a = dict(task_a, id="devtask_a", description="A")
    task_b = dict(task_b, id="devtask_b", description="B")
    response = await async_client.post(
        "/dev/resolve_conflict",
        json={"task_a": task_a, "task_b": task_b},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 200
    winner = response.json()["resolved_task"]["id"]
    assert (winner == "devtask_a" if expected == "task_a" else winner == "devtask_b")
