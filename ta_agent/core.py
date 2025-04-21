from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
import uuid
import json
from redis.asyncio import Redis
import asyncio

class ArchitectureDecision(BaseModel):
    id: str
    summary: str
    rationale: Optional[str]
    status: str = "pending"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    context: Optional[Dict] = None
    dependencies: Optional[List[str]] = []
    priority: Optional[int] = 1
    timestamp: float = datetime.now().timestamp()

class TAStateManager:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        self.redis = Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.aredis = Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.decision_registry = "ta:decisions"
        # Circuit breaker state
        self.circuit_open = False
        self.failure_count = 0
        self.failure_threshold = 5
        self.bulkhead_semaphore = asyncio.Semaphore(10)

    def create_decision(self, decision: dict) -> str:
        decision = decision.copy()
        for k in ['created_at', 'updated_at']:
            if k in decision and hasattr(decision[k], 'isoformat'):
                decision[k] = decision[k].isoformat()
        decision_id = f"decision_{uuid.uuid4().hex}"
        self.redis.hset(self.decision_registry, decision_id, json.dumps(decision))
        return decision_id

    async def async_create_decision(self, decision: dict) -> str:
        if self.circuit_open:
            raise Exception("Redis circuit breaker open")
        async with self.bulkhead_semaphore:
            try:
                decision = decision.copy()
                for k in ['created_at', 'updated_at']:
                    if k in decision and hasattr(decision[k], 'isoformat'):
                        decision[k] = decision[k].isoformat()
                decision_id = f"decision_{uuid.uuid4().hex}"
                await self.aredis.hset(self.decision_registry, decision_id, json.dumps(decision))
                self.failure_count = 0
                return decision_id
            except Exception as e:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.circuit_open = True
                raise e

    def get_decision(self, decision_id: str) -> dict:
        raw = self.redis.hget(self.decision_registry, decision_id)
        if not raw:
            return None
        return json.loads(raw)

    async def async_get_decision(self, decision_id: str) -> dict:
        if self.circuit_open:
            raise Exception("Redis circuit breaker open")
        async with self.bulkhead_semaphore:
            try:
                raw = await self.aredis.hget(self.decision_registry, decision_id)
                self.failure_count = 0
                return json.loads(raw) if raw else None
            except Exception as e:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.circuit_open = True
                raise e

    def list_decisions(self) -> list:
        keys = self.redis.hkeys(self.decision_registry)
        return [json.loads(self.redis.hget(self.decision_registry, k)) for k in keys]

    async def async_list_decisions(self) -> list:
        if self.circuit_open:
            raise Exception("Redis circuit breaker open")
        async with self.bulkhead_semaphore:
            try:
                keys = await self.aredis.hkeys(self.decision_registry)
                self.failure_count = 0
                return [json.loads(await self.aredis.hget(self.decision_registry, k)) for k in keys]
            except Exception as e:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.circuit_open = True
                raise e

    def update_decision(self, decision_id: str, updates: dict) -> None:
        decision = self.get_decision(decision_id)
        if not decision:
            raise ValueError("Decision not found")
        decision.update(updates)
        for k in ['created_at', 'updated_at']:
            if k in decision and hasattr(decision[k], 'isoformat'):
                decision[k] = decision[k].isoformat()
        self.redis.hset(self.decision_registry, decision_id, json.dumps(decision))

    async def async_update_decision(self, decision_id: str, updates: dict) -> None:
        if self.circuit_open:
            raise Exception("Redis circuit breaker open")
        async with self.bulkhead_semaphore:
            try:
                decision = await self.async_get_decision(decision_id)
                if not decision:
                    raise ValueError("Decision not found")
                decision.update(updates)
                for k in ['created_at', 'updated_at']:
                    if k in decision and hasattr(decision[k], 'isoformat'):
                        decision[k] = decision[k].isoformat()
                await self.aredis.hset(self.decision_registry, decision_id, json.dumps(decision))
                self.failure_count = 0
            except Exception as e:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.circuit_open = True
                raise e

    def resolve_conflict(self, dec_a: dict, dec_b: dict, alpha: float = 0.7, beta: float = 0.3) -> dict:
        time_score = alpha * (dec_a.get('timestamp', 0) - dec_b.get('timestamp', 0))
        priority_score = beta * (dec_a.get('priority', 1) - dec_b.get('priority', 1))
        return dec_a if (time_score + priority_score) >= 0 else dec_b

    async def async_batch_update_decisions(self, updates: list, batch_size: int = 50) -> list:
        if self.circuit_open:
            raise Exception("Redis circuit breaker open")
        updated_ids = []
        for i in range(0, len(updates), batch_size):
            batch = updates[i:i+batch_size]
            pipe = self.aredis.pipeline()
            for upd in batch:
                decision_id = upd['id']
                raw = await self.aredis.hget(self.decision_registry, decision_id)
                if raw:
                    decision = json.loads(raw)
                    decision.update(upd)
                    pipe.hset(self.decision_registry, decision_id, json.dumps(decision))
                    updated_ids.append(decision_id)
            await pipe.execute()
        self.failure_count = 0
        return updated_ids
