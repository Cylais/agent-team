import uuid
import json
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, validator
import redis.asyncio as redis
from opentelemetry import trace

class DevTask(BaseModel):
    id: str
    description: str
    assigned_to: Optional[str]
    status: str = "pending"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    context: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[str]] = []
    priority: Optional[int] = 1
    timestamp: float = datetime.now().timestamp()

    class Config:
        schema_extra = {
            "example": {
                "id": "devtask_123",
                "description": "Implement login feature",
                "assigned_to": "developer1",
                "status": "pending",
                "priority": 2
            }
        }

    @validator("status")
    def status_must_be_valid(cls, v):
        valid_statuses = ["pending", "in_progress", "completed", "blocked"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return v

from .circuit import redis_circuit_breaker

from .ai_hints import AIHintEngine

class DevStateManager:
    """
    State manager for developer agent tasks using async Redis with connection pooling, circuit breaker protection, batch pipelining, and context-aware AI hints for task creation.
    """
    def __init__(self, redis_url: str = None):
        """
        Initialize DevStateManager with a robust, tuned Redis connection pool.

        Pool parameters can be set via environment variables for flexibility:
        - DEV_AGENT_REDIS_URL (default: 'redis://localhost:6379')
        - DEV_AGENT_REDIS_MAX_CONNECTIONS (default: 100, int, min 1, recommended <= 1000)
        - DEV_AGENT_REDIS_SOCKET_KEEPALIVE (default: True, bool)
        - DEV_AGENT_REDIS_RETRY_ON_TIMEOUT (default: True, bool)
        - DEV_AGENT_REDIS_SOCKET_CONNECT_TIMEOUT (default: 3, float, seconds)
        - DEV_AGENT_REDIS_SOCKET_TIMEOUT (default: 5, float, seconds)

        Example:
            export DEV_AGENT_REDIS_MAX_CONNECTIONS=200
            export DEV_AGENT_REDIS_SOCKET_KEEPALIVE=False
        """
        import os
        import logging
        logger = logging.getLogger("dev_agent.core")
        redis_url = redis_url or os.getenv("DEV_AGENT_REDIS_URL", "redis://localhost:6379")
        # Validate and sanitize parameters
        try:
            max_connections = int(os.getenv("DEV_AGENT_REDIS_MAX_CONNECTIONS", 100))
            if max_connections < 1:
                logger.warning("DEV_AGENT_REDIS_MAX_CONNECTIONS < 1, resetting to 1")
                max_connections = 1
            if max_connections > 1000:
                logger.warning("DEV_AGENT_REDIS_MAX_CONNECTIONS > 1000, capping at 1000")
                max_connections = 1000
        except Exception:
            logger.warning("Invalid DEV_AGENT_REDIS_MAX_CONNECTIONS, using default 100")
            max_connections = 100
        socket_keepalive = os.getenv("DEV_AGENT_REDIS_SOCKET_KEEPALIVE", "True").lower() == "true"
        retry_on_timeout = os.getenv("DEV_AGENT_REDIS_RETRY_ON_TIMEOUT", "True").lower() == "true"
        try:
            socket_connect_timeout = float(os.getenv("DEV_AGENT_REDIS_SOCKET_CONNECT_TIMEOUT", 3))
            if socket_connect_timeout < 0:
                logger.warning("DEV_AGENT_REDIS_SOCKET_CONNECT_TIMEOUT < 0, resetting to 0")
                socket_connect_timeout = 0
        except Exception:
            logger.warning("Invalid DEV_AGENT_REDIS_SOCKET_CONNECT_TIMEOUT, using default 3")
            socket_connect_timeout = 3
        try:
            socket_timeout = float(os.getenv("DEV_AGENT_REDIS_SOCKET_TIMEOUT", 5))
            if socket_timeout < 0:
                logger.warning("DEV_AGENT_REDIS_SOCKET_TIMEOUT < 0, resetting to 0")
                socket_timeout = 0
        except Exception:
            logger.warning("Invalid DEV_AGENT_REDIS_SOCKET_TIMEOUT, using default 5")
            socket_timeout = 5
        self.task_registry = "dev:tasks"
        logger.info(f"[Redis Pool Settings] url={redis_url} max_connections={max_connections} keepalive={socket_keepalive} retry_on_timeout={retry_on_timeout} connect_timeout={socket_connect_timeout} timeout={socket_timeout}")
        self.redis = redis.Redis.from_url(
            redis_url,
            decode_responses=True,
            max_connections=max_connections,
            socket_keepalive=socket_keepalive,
            retry_on_timeout=retry_on_timeout,
            socket_connect_timeout=socket_connect_timeout,
            socket_timeout=socket_timeout
        )
        self.ai_hint_engine = AIHintEngine(self.redis)


    async def suggest_task_fields(self, description: str, context: dict) -> dict:
        """
        Suggest context-aware fields for a new task based on semantic and heuristic analysis.
        Returns a dict with possible values for priority, dependencies, assigned_to, etc.
        """
        return await self.ai_hint_engine.suggest_task_fields(description, context)


    @redis_circuit_breaker
    async def create_task(self, task: dict) -> str:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Redis Create Task"):
            task = task.copy()
            for k in ['created_at', 'updated_at']:
                if k in task and hasattr(task[k], 'isoformat'):
                    task[k] = task[k].isoformat()
            task_id = f"devtask_{uuid.uuid4().hex}"
            await self.redis.hset(self.task_registry, task_id, json.dumps(task))
            return task_id

    @redis_circuit_breaker
    async def get_task(self, task_id: str) -> Optional[dict]:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Redis Get Task"):
            raw = await self.redis.hget(self.task_registry, task_id)
            if not raw:
                return None
            return json.loads(raw)

    @redis_circuit_breaker
    async def list_tasks(self) -> List[dict]:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Redis List Tasks"):
            keys = await self.redis.hkeys(self.task_registry)
            if not keys:
                return []
            pipe = self.redis.pipeline()
            for k in keys:
                pipe.hget(self.task_registry, k)
            raw_tasks = await pipe.execute()
            return [json.loads(raw) for raw in raw_tasks if raw]

    @redis_circuit_breaker
    async def update_task(self, task_id: str, updates: dict) -> dict:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Redis Update Task"):
            raw = await self.redis.hget(self.task_registry, task_id)
            if not raw:
                raise ValueError("Task not found")
            task = json.loads(raw)
            task.update(updates)
            task['updated_at'] = datetime.now().isoformat()
            await self.redis.hset(self.task_registry, task_id, json.dumps(task))
            return task

    @redis_circuit_breaker
    async def delete_task(self, task_id: str) -> None:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Redis Delete Task"):
            await self.redis.hdel(self.task_registry, task_id)

    import logging

    async def resolve_conflict(self, task_a: dict, task_b: dict) -> dict:
        """
        Resolve conflict between two tasks using semantic similarity and rule-based scoring.
        If tasks are highly similar, prefer by priority and recency. Logs the decision path.
        """
        logger = logging.getLogger("dev_agent.conflict")
        # Prefer completed status
        if task_a.get("status") == "completed" and task_b.get("status") != "completed":
            logger.info("Conflict resolved: task_a is completed, task_b is not.")
            return task_a
        if task_b.get("status") == "completed" and task_a.get("status") != "completed":
            logger.info("Conflict resolved: task_b is completed, task_a is not.")
            return task_b
        # Compute semantic similarity
        desc_a = task_a.get("description", "")
        desc_b = task_b.get("description", "")
        similarity = 0.0
        try:
            similarity = await self.ai_hint_engine.semantic_similarity(desc_a, desc_b)
        except Exception as e:
            logger.warning(f"Semantic similarity computation failed: {e}")
        logger.info(f"Semantic similarity between tasks: {similarity:.2f}")
        # If highly similar, prefer by priority then recency
        similarity_threshold = 0.7
        if similarity >= similarity_threshold:
            pa, pb = task_a.get("priority", 1), task_b.get("priority", 1)
            if pa != pb:
                winner = task_a if pa > pb else task_b
                logger.info(f"Conflict resolved: tasks similar, higher priority wins. Winner: {'A' if winner is task_a else 'B'}")
                return winner
            # If priorities equal, prefer more recent timestamp
            ta, tb = task_a.get("timestamp", 0), task_b.get("timestamp", 0)
            winner = task_a if ta >= tb else task_b
            logger.info(f"Conflict resolved: tasks similar, priorities equal, more recent timestamp wins. Winner: {'A' if winner is task_a else 'B'}")
            return winner
        # Otherwise, use rule-based scoring
        time_score = 0.5 * (task_a.get("timestamp", 0) - task_b.get("timestamp", 0))
        priority_score = 0.3 * (task_a.get("priority", 1) - task_b.get("priority", 1))
        dep_score = 0.2 * (len(task_a.get("dependencies", [])) - len(task_b.get("dependencies", [])))
        total_score = time_score + priority_score + dep_score
        winner = task_a if total_score >= 0 else task_b
        logger.info(f"Conflict resolved: rule-based scoring. Winner: {'A' if winner is task_a else 'B'} | Score: {total_score:.2f}")
        return winner

    @redis_circuit_breaker
    async def batch_update_tasks(self, updates: List[dict], batch_size: int = 50) -> List[str]:
        """
        Efficiently update multiple tasks in Redis using pipelining.
        Args:
            updates: List of dicts, each with at least 'id' and update fields.
            batch_size: Number of updates per pipeline execution.
        Returns:
            List of updated task IDs.
        Raises:
            ValueError if any update lacks an 'id'.
        """
        updated_ids = []
        for i in range(0, len(updates), batch_size):
            batch = updates[i:i+batch_size]
            pipe = self.redis.pipeline()
            for upd in batch:
                task_id = upd.get('id')
                if not task_id:
                    raise ValueError("Each update dict must include an 'id' key")
                # Fetch, update, and re-serialize
                pipe.hget(self.task_registry, task_id)
            raws = await pipe.execute()
            pipe = self.redis.pipeline()
            for upd, raw in zip(batch, raws):
                task_id = upd['id']
                if raw:
                    task = json.loads(raw)
                    task.update(upd)
                    for k in ['created_at', 'updated_at']:
                        if k in task and hasattr(task[k], 'isoformat'):
                            task[k] = task[k].isoformat()
                    pipe.hset(self.task_registry, task_id, json.dumps(task))
                    updated_ids.append(task_id)
            await pipe.execute()
        return updated_ids
