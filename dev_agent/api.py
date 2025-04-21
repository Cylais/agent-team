from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from .core import DevStateManager, DevTask
from .security import validate_jwt
from .rate_limit import default_rate_limiter
import uuid

# Dependency injection for DevStateManager
async def get_state_manager() -> DevStateManager:
    return DevStateManager()

dev_router = APIRouter(prefix="/dev", tags=["Developer"])

class DevTaskRequest(BaseModel):
    description: str
    assigned_to: Optional[str] = None
    context: Dict[str, Any]
    dependencies: List[str] = []
    priority: int = 1

class DevTaskUpdate(BaseModel):
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[str]] = None
    priority: Optional[int] = None


from fastapi import Query

@dev_router.post("/create_task", status_code=201, dependencies=[Depends(validate_jwt), Depends(default_rate_limiter())])
async def create_task(
    req: DevTaskRequest,
    state_manager: DevStateManager = Depends(get_state_manager),
    enable_ai_hints: bool = Query(False, description="Enable AI hints for task field suggestions"),
    preview: bool = Query(False, description="Preview suggested fields without creating task")
):
    """
    Create a new developer task, optionally using AI hints for field suggestion. Supports preview mode for suggestions.
    """
    task_data = req.dict()
    suggestions = {}
    # AI hint logic
    if enable_ai_hints:
        suggestions = await state_manager.suggest_task_fields(req.description, req.context)
        # Only update fields if not already set in request
        for k, v in suggestions.items():
            if k not in task_data or not task_data[k]:
                task_data[k] = v
    if preview:
        return {"proposed_task": task_data, "suggestions": suggestions}
    # Create and persist the task
    task = DevTask(
        id=f"devtask_{uuid.uuid4().hex}",
        description=task_data["description"],
        assigned_to=task_data.get("assigned_to"),
        status="pending",
        context=task_data.get("context"),
        dependencies=task_data.get("dependencies", []),
        priority=task_data.get("priority", 1)
    )
    task_id = await state_manager.create_task(task.dict())
    return {"task_id": task_id, "applied_suggestions": suggestions}

@dev_router.post("/suggest_task_fields", dependencies=[Depends(validate_jwt), Depends(default_rate_limiter())])
async def suggest_task_fields(
    req: DevTaskRequest,
    state_manager: DevStateManager = Depends(get_state_manager)
):
    """
    Preview AI-generated suggestions for task fields based on description and context.
    """
    suggestions = await state_manager.suggest_task_fields(req.description, req.context)
    return {"suggestions": suggestions}


@dev_router.get("/status/{task_id}", dependencies=[Depends(validate_jwt), Depends(default_rate_limiter())])
async def get_task_status(task_id: str, state_manager: DevStateManager = Depends(get_state_manager)):
    """
    Get the status of a developer task by ID. Rate limited per user/IP.
    """
    task = await state_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}

@dev_router.get("/list", dependencies=[Depends(validate_jwt), Depends(default_rate_limiter())])
async def list_tasks(state_manager: DevStateManager = Depends(get_state_manager)):
    """
    List all developer tasks. Rate limited per user/IP.
    """
    tasks = await state_manager.list_tasks()
    return {"tasks": tasks}

@dev_router.put("/task/{task_id}", dependencies=[Depends(validate_jwt), Depends(default_rate_limiter())])
async def update_task(task_id: str, updates: DevTaskUpdate, state_manager: DevStateManager = Depends(get_state_manager)):
    """
    Update a developer task. Rate limited per user/IP.
    """
    try:
        updated_task = await state_manager.update_task(task_id, updates.dict(exclude_unset=True))
        return {"task": updated_task}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@dev_router.delete("/task/{task_id}", dependencies=[Depends(validate_jwt)])
async def delete_task(task_id: str, state_manager: DevStateManager = Depends(get_state_manager)):
    await state_manager.delete_task(task_id)
    return {"status": "deleted"}

@dev_router.post("/resolve_conflict", dependencies=[Depends(validate_jwt)])
async def resolve_conflict(task_a: Dict, task_b: Dict, state_manager: DevStateManager = Depends(get_state_manager)):
    resolved = await state_manager.resolve_conflict(task_a, task_b)
    return {"resolved_task": resolved}
