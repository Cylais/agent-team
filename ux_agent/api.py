from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from .core import UXStateManager, UXFeedback
import uuid

ux_router = APIRouter(prefix="/ux", tags=["User Experience"])
ux_state = UXStateManager()

class UXFeedbackRequest(BaseModel):
    description: str
    assigned_to: Optional[str] = None
    context: Dict[str, Any]
    dependencies: List[str] = []
    priority: int = 1

@ux_router.post("/create_feedback", status_code=201)
async def create_feedback(req: UXFeedbackRequest):
    feedback = UXFeedback(
        id=f"uxfb_{uuid.uuid4().hex}",
        description=req.description,
        assigned_to=req.assigned_to,
        status="pending",
        context=req.context,
        dependencies=req.dependencies,
        priority=req.priority
    )
    feedback_id = ux_state.create_feedback(feedback.dict())
    return {"feedback_id": feedback_id}

@ux_router.get("/status/{feedback_id}")
async def get_feedback_status(feedback_id: str):
    feedback = ux_state.get_feedback(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"feedback": feedback}

@ux_router.post("/resolve_conflict")
async def resolve_conflict(feedback_a: Dict, feedback_b: Dict):
    resolved = ux_state.resolve_conflict(feedback_a, feedback_b)
    return {"resolved_feedback": resolved}
