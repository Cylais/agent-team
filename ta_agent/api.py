from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from .security import validate_jwt
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from .core import TAStateManager, ArchitectureDecision
from fastapi import BackgroundTasks
import uuid

ta_router = APIRouter(prefix="/ta", tags=["Technical Architect"])
ta_state = TAStateManager()

class DecisionRequest(BaseModel):
    summary: str
    rationale: Optional[str] = None
    context: Dict[str, Any]
    dependencies: List[str] = []
    priority: int = 1

@ta_router.post("/propose_decision", status_code=201)
async def propose_decision(req: DecisionRequest):
    decision = ArchitectureDecision(
        id=f"decision_{uuid.uuid4().hex}",
        summary=req.summary,
        rationale=req.rationale,
        status="pending",
        context=req.context,
        dependencies=req.dependencies,
        priority=req.priority
    )
    decision_id = ta_state.create_decision(decision.dict())
    return {"decision_id": decision_id}

@ta_router.post("/async_propose_decision", status_code=201, dependencies=[Depends(validate_jwt), Depends(RateLimiter(times=5, seconds=60))])
async def async_propose_decision(req: DecisionRequest):
    decision = ArchitectureDecision(
        id=f"decision_{uuid.uuid4().hex}",
        summary=req.summary,
        rationale=req.rationale,
        status="pending",
        context=req.context,
        dependencies=req.dependencies,
        priority=req.priority
    )
    decision_id = await ta_state.async_create_decision(decision.dict())
    return {"decision_id": decision_id}

@ta_router.get("/async_status/{decision_id}", dependencies=[Depends(validate_jwt), Depends(RateLimiter(times=10, seconds=60))])
async def async_get_decision_status(decision_id: str):
    decision = await ta_state.async_get_decision(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return {"decision": decision}

@ta_router.get("/async_list_decisions", dependencies=[Depends(validate_jwt), Depends(RateLimiter(times=10, seconds=60))])
async def async_list_decisions():
    decisions = await ta_state.async_list_decisions()
    return {"decisions": decisions}

@ta_router.post("/async_update_decision/{decision_id}", dependencies=[Depends(validate_jwt), Depends(RateLimiter(times=5, seconds=60))])
async def async_update_decision(decision_id: str, updates: Dict):
    await ta_state.async_update_decision(decision_id, updates)
    return {"status": "updated"}

@ta_router.post("/async_batch_update_decisions", dependencies=[Depends(validate_jwt), Depends(RateLimiter(times=2, seconds=60))])
async def async_batch_update_decisions(updates: List[Dict]):
    updated_ids = await ta_state.async_batch_update_decisions(updates)
    return {"updated_ids": updated_ids}

@ta_router.post("/ai_hint", dependencies=[Depends(validate_jwt), Depends(RateLimiter(times=5, seconds=60))])
async def ai_hint(objective: str, context: Dict):
    # Placeholder for AI/semantic hint logic
    return {"suggested_fields": {"priority": 1, "dependencies": []}}


@ta_router.get("/status/{decision_id}")
async def get_decision_status(decision_id: str):
    decision = ta_state.get_decision(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return {"decision": decision}

@ta_router.post("/resolve_conflict")
async def resolve_conflict(dec_a: Dict, dec_b: Dict):
    resolved = ta_state.resolve_conflict(dec_a, dec_b)
    return {"resolved_decision": resolved}
