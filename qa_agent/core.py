from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
import uuid
import json
import redis.asyncio as aioredis
import asyncio

class QATestCase(BaseModel):
    id: str
    description: str
    assigned_to: Optional[str]
    status: str = "pending"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    context: Optional[Dict] = None
    dependencies: Optional[List[str]] = []
    priority: Optional[int] = 1
    timestamp: float = datetime.now().timestamp()

class QAStateManager:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379, max_concurrent: int = 10):
        self.redis = aioredis.from_url(f"redis://{redis_host}:{redis_port}/0", decode_responses=True)
        self.test_registry = "qa:tests"
        self.bulkhead = asyncio.Semaphore(max_concurrent)
        self.circuit_open = False
        self.fail_count = 0
        self.max_failures = 3
        self.reset_timeout = 5  # seconds

    async def _circuit_breaker(self, coro):
        if self.circuit_open:
            raise Exception("Redis circuit breaker is open")
        try:
            async with self.bulkhead:
                result = await coro
            self.fail_count = 0
            return result
        except Exception as e:
            self.fail_count += 1
            if self.fail_count >= self.max_failures:
                self.circuit_open = True
                asyncio.create_task(self._reset_circuit())
            raise e

    async def _reset_circuit(self):
        await asyncio.sleep(self.reset_timeout)
        self.circuit_open = False
        self.fail_count = 0

    def create_test(self, test: dict) -> str:
        test = test.copy()
        for k in ['created_at', 'updated_at']:
            if k in test and hasattr(test[k], 'isoformat'):
                test[k] = test[k].isoformat()
        test_id = f"qatest_{uuid.uuid4().hex}"
        self.redis.hset(self.test_registry, test_id, json.dumps(test))
        return test_id

    async def async_create_test(self, test: dict) -> str:
        test = test.copy()
        for k in ['created_at', 'updated_at']:
            if k in test and hasattr(test[k], 'isoformat'):
                test[k] = test[k].isoformat()
        test_id = f"qatest_{uuid.uuid4().hex}"
        await self._circuit_breaker(self.redis.hset(self.test_registry, test_id, json.dumps(test)))
        return test_id

    def get_test(self, test_id: str) -> dict:
        raw = self.redis.hget(self.test_registry, test_id)
        if not raw:
            return None
        return json.loads(raw)

    async def async_get_test(self, test_id: str) -> dict:
        raw = await self._circuit_breaker(self.redis.hget(self.test_registry, test_id))
        if not raw:
            return None
        return json.loads(raw)

    def list_tests(self) -> list:
        keys = self.redis.hkeys(self.test_registry)
        return [json.loads(self.redis.hget(self.test_registry, k)) for k in keys]

    async def async_list_tests(self) -> list:
        keys = await self._circuit_breaker(self.redis.hkeys(self.test_registry))
        return [json.loads(await self._circuit_breaker(self.redis.hget(self.test_registry, k))) for k in keys]

    def update_test(self, test_id: str, updates: dict) -> None:
        test = self.get_test(test_id)
        if not test:
            raise ValueError("Test not found")
        test.update(updates)
        for k in ['created_at', 'updated_at']:
            if k in test and hasattr(test[k], 'isoformat'):
                test[k] = test[k].isoformat()
        self.redis.hset(self.test_registry, test_id, json.dumps(test))

    async def async_update_test(self, test_id: str, updates: dict) -> None:
        test = await self.async_get_test(test_id)
        if not test:
            raise ValueError("Test not found")
        test.update(updates)
        for k in ['created_at', 'updated_at']:
            if k in test and hasattr(test[k], 'isoformat'):
                test[k] = test[k].isoformat()
        await self._circuit_breaker(self.redis.hset(self.test_registry, test_id, json.dumps(test)))

    def resolve_conflict(self, test_a: dict, test_b: dict, alpha: float = 0.7, beta: float = 0.3) -> dict:
        time_score = alpha * (test_a.get('timestamp', 0) - test_b.get('timestamp', 0))
        priority_score = beta * (test_a.get('priority', 1) - test_b.get('priority', 1))
        return test_a if (time_score + priority_score) >= 0 else test_b

    async def async_resolve_conflict(self, test_a: dict, test_b: dict, alpha: float = 0.7, beta: float = 0.3) -> dict:
        return self.resolve_conflict(test_a, test_b, alpha, beta)
