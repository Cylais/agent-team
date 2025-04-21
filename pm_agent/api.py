from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from .core import PMStateManager, Task
from .batch_ai_semantic import PMBatchHelper, PMAIHintEngine, semantic_conflict_resolution
from fastapi_limiter.depends import RateLimiter
import uuid
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBearer
from .security import validate_jwt
import asyncio

pm_router = APIRouter(prefix="/pm", tags=["Project Management"])
pm_state = PMStateManager()
batch_helper = PMBatchHelper(pm_state.aredis)
ai_hint_engine = PMAIHintEngine(pm_state.aredis)
prometheus_instrumentator = Instrumentator()
security = HTTPBearer()

@pm_router.get("/metrics", include_in_schema=False)
async def metrics():
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

class TaskRequest(BaseModel):
    objective: str
    context: Dict[str, Any]
    dependencies: List[str] = []
    assigned_to: Optional[str] = None
    priority: int = 1

@pm_router.post("/assign_task", status_code=201, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def assign_task(req: TaskRequest, token=Depends(validate_jwt)):
    task = Task(
        id=f"task_{uuid.uuid4().hex}",
        objective=req.objective,
        assigned_to=req.assigned_to,
        status="pending",
        context=req.context,
        dependencies=req.dependencies,
        priority=req.priority
    )
    task_id = await pm_state.async_create_task(task.dict())
    return {"task_id": task_id}

@pm_router.get("/status/{task_id}", dependencies=[Depends(RateLimiter(times=30, seconds=60))])
async def get_task_status(task_id: str, token=Depends(validate_jwt)):
    task = await pm_state.async_get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}

@pm_router.post("/resolve_conflict", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def resolve_conflict(task_a: Dict, task_b: Dict, token=Depends(validate_jwt)):
    # Use semantic conflict resolution
    resolved = semantic_conflict_resolution(task_a, task_b)
    return {"resolved_task": resolved}

# --- Batch update endpoint ---
@pm_router.post("/batch_update", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def batch_update(updates: List[Dict], token=Depends(validate_jwt)):
    updated_ids = await batch_helper.batch_update_tasks(updates)
    return {"updated_ids": updated_ids}

# --- AI/semantic task hint endpoint ---
@pm_router.post("/ai_hint", dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def ai_hint(objective: str, context: Dict, token=Depends(validate_jwt)):
    hints = await ai_hint_engine.suggest_task_fields(objective, context)
    return {"hints": hints}
