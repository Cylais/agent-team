from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
import uuid
import json
import redis.asyncio as aioredis
from redis import Redis  # legacy, for migration
import asyncio
import logging
from prometheus_client import Counter, Gauge
from opentelemetry import trace
from opentelemetry.instrumentation.redis import RedisInstrumentor

class Task(BaseModel):
    id: str
    objective: str
    assigned_to: Optional[str]
    status: str = "pending"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    context: Optional[Dict] = None
    dependencies: Optional[List[str]] = []
    priority: Optional[int] = 1
    timestamp: float = datetime.now().timestamp()

class PMStateManager:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        # Legacy sync Redis for migration
        self.redis = Redis(host=redis_host, port=redis_port, decode_responses=True)
        # Async Redis for new operations
        self.aredis = aioredis.from_url(f"redis://{redis_host}:{redis_port}", decode_responses=True)
        self.task_registry = "pm:tasks"
        # Circuit breaker state
        self.circuit_open = False
        self.failure_count = 0
        self.failure_threshold = 3
        self.recovery_timeout = 10  # seconds
        self.last_failure_time = None
        # Prometheus metrics
        self.task_create_counter = Counter('pm_task_create_total', 'Total PM tasks created')
        self.conflict_resolve_counter = Counter('pm_conflict_resolve_total', 'Total PM conflicts resolved')
        self.redis_circuit_gauge = Gauge('pm_redis_circuit_open', 'PM Redis circuit breaker state')
        # OpenTelemetry tracer
        self.tracer = trace.get_tracer(__name__)
        RedisInstrumentor().instrument()
        # Logging
        self.logger = logging.getLogger("pm_agent.PMStateManager")

    # --- Legacy sync methods below (to be migrated) ---

    def create_task(self, task: dict) -> str:
        # ... (existing sync code)
        task = task.copy()
        for k in ['created_at', 'updated_at']:
            if k in task and hasattr(task[k], 'isoformat'):
                task[k] = task[k].isoformat()
        task_id = f"task_{uuid.uuid4().hex}"
        self.redis.hset(self.task_registry, task_id, json.dumps(task))
        return task_id

    # --- Modern async methods below ---

    async def async_create_task(self, task: dict) -> str:
        with self.tracer.start_as_current_span("pm_async_create_task"):
            if self.circuit_open:
                self.logger.warning("Circuit breaker open: rejecting create_task")
                raise Exception("Redis circuit breaker open")
            try:
                task = task.copy()
                for k in ['created_at', 'updated_at']:
                    if k in task and hasattr(task[k], 'isoformat'):
                        task[k] = task[k].isoformat()
                task_id = f"task_{uuid.uuid4().hex}"
                await self.aredis.hset(self.task_registry, task_id, json.dumps(task))
                self.task_create_counter.inc()
                self.logger.info(f"Task created: {task_id}")
                self._reset_circuit()
                return task_id
            except Exception as e:
                self._record_failure()
                self.logger.error(f"Create task failed: {e}")
                raise

    async def async_get_task(self, task_id: str) -> dict:
        with self.tracer.start_as_current_span("pm_async_get_task"):
            if self.circuit_open:
                self.logger.warning("Circuit breaker open: rejecting get_task")
                raise Exception("Redis circuit breaker open")
            try:
                raw = await self.aredis.hget(self.task_registry, task_id)
                self._reset_circuit()
                if not raw:
                    return None
                return json.loads(raw)
            except Exception as e:
                self._record_failure()
                self.logger.error(f"Get task failed: {e}")
                raise

    async def async_update_task(self, task_id: str, updates: dict) -> None:
        with self.tracer.start_as_current_span("pm_async_update_task"):
            if self.circuit_open:
                self.logger.warning("Circuit breaker open: rejecting update_task")
                raise Exception("Redis circuit breaker open")
            try:
                task = await self.async_get_task(task_id)
                if not task:
                    raise ValueError("Task not found")
                task.update(updates)
                await self.aredis.hset(self.task_registry, task_id, json.dumps(task))
                self._reset_circuit()
                self.logger.info(f"Task updated: {task_id}")
            except Exception as e:
                self._record_failure()
                self.logger.error(f"Update task failed: {e}")
                raise

    async def async_resolve_conflict(self, task_a: dict, task_b: dict, alpha: float = 0.7, beta: float = 0.3) -> dict:
        with self.tracer.start_as_current_span("pm_async_resolve_conflict"):
            self.conflict_resolve_counter.inc()
            # Example: log and use same logic as sync for now
            self.logger.info(f"Resolving conflict: {task_a['id']} vs {task_b['id']}")
            time_score = alpha * (task_a.get('timestamp', 0) - task_b.get('timestamp', 0))
            priority_score = beta * (task_a.get('priority', 1) - task_b.get('priority', 1))
            resolved = task_a if (time_score + priority_score) >= 0 else task_b
            self.logger.info(f"Conflict resolved: {resolved['id']}")
            return resolved

    # --- Circuit breaker helpers ---
    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = asyncio.get_event_loop().time()
        if self.failure_count >= self.failure_threshold:
            self.circuit_open = True
            self.redis_circuit_gauge.set(1)
            self.logger.error("Redis circuit breaker opened!")

    def _reset_circuit(self):
        self.failure_count = 0
        self.circuit_open = False
        self.redis_circuit_gauge.set(0)

    async def circuit_breaker_monitor(self):
        while True:
            if self.circuit_open and self.last_failure_time:
                now = asyncio.get_event_loop().time()
                if now - self.last_failure_time > self.recovery_timeout:
                    self._reset_circuit()
                    self.logger.info("Redis circuit breaker reset.")
            await asyncio.sleep(1)

    def create_task(self, task: dict) -> str:
        # Ensure all fields are JSON serializable
        task = task.copy()
        for k in ['created_at', 'updated_at']:
            if k in task and hasattr(task[k], 'isoformat'):
                task[k] = task[k].isoformat()
        task_id = f"task_{uuid.uuid4().hex}"
        self.redis.hset(self.task_registry, task_id, json.dumps(task))
        return task_id

    def get_task(self, task_id: str) -> dict:
        raw = self.redis.hget(self.task_registry, task_id)
        if not raw:
            return None
        return json.loads(raw)

    def list_tasks(self) -> list:
        # This is a simplified scan; in production, use SCAN for large sets
        keys = self.redis.keys(f"{self.task_registry}:*")
        return [self.redis.json().get(k) for k in keys]

    def update_task(self, task_id: str, updates: dict) -> None:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("Task not found")
        task.update(updates)
        self.redis.json().set(f"{self.task_registry}:{task_id}", Path.root_path(), task)

    def resolve_conflict(self, task_a: dict, task_b: dict, alpha: float = 0.7, beta: float = 0.3) -> dict:
        time_score = alpha * (task_a.get('timestamp', 0) - task_b.get('timestamp', 0))
        priority_score = beta * (task_a.get('priority', 1) - task_b.get('priority', 1))
        return task_a if (time_score + priority_score) >= 0 else task_b
