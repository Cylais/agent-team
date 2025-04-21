from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

router = APIRouter()

# --- Instruction Ingestion ---
class InstructionPayload(BaseModel):
    sender: str = Field(..., example="PM")
    recipient: str = Field(..., example="DEV")
    type: str = Field(..., example="task")
    correlation_id: str
    timestamp: str
    payload: Dict[str, Any]
    priority: Optional[str] = Field("normal", example="high")
    metadata: Optional[Dict[str, Any]] = None

@router.post("/agent/send", status_code=status.HTTP_200_OK)
async def send_instruction(payload: InstructionPayload, request: Request):
    # Simulate ingestion logic and echo back for mock
    cid = request.headers.get("X-Correlation-ID", payload.correlation_id)
    response = JSONResponse({"status": "received", "echo": payload.dict()})
    response.headers["X-Correlation-ID"] = cid
    return response

# --- Build Status Webhook ---
class BuildStatusPayload(BaseModel):
    build_id: str
    status: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

@router.post("/agent/build_status", status_code=status.HTTP_200_OK)
async def build_status(payload: BuildStatusPayload):
    # Simulate status update
    return {"status": "ok", "build_id": payload.build_id, "received_status": payload.status}

# --- Session Control Endpoints ---
class SessionControlPayload(BaseModel):
    session_id: str
    action: str  # start, pause, terminate
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

@router.post("/agent/session_control", status_code=status.HTTP_200_OK)
async def session_control(payload: SessionControlPayload):
    # Simulate session control
    return {"status": "ok", "session_id": payload.session_id, "action": payload.action}
