"""
Context-Adaptive Agent API Example (Proof of Concept)
"""
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI()

class ContextPayload(BaseModel):
    """
    Payload schema for context-adaptive decision endpoint.
    """
    user_role: str
    time_of_day: str
    agent_state: str
    data: Dict[str, Any] = {}

from fastapi import Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional, List

class ErrorResponse(BaseModel):
    """
    Standardized error response model.
    """
    error: str
    detail: Optional[str] = None

@app.post("/agent/contextual_decision", tags=["Context Adaptation"])
async def contextual_decision(
    payload: ContextPayload,
    request: Request,
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to include in the response (field masking)")
) -> Any:
    """
    Context-adaptive decision endpoint.

    Responds differently based on context (role, time, state).
    Supports flexible return shapes via field masking (?fields=decision,note).
    Returns error responses with a clear schema on validation or logic errors.

    Args:
        payload (ContextPayload): Input context for the decision.
        request (Request): FastAPI request object (unused, but available for future context).
        fields (Optional[str]): Comma-separated list of fields to include in the response.

    Returns:
        Dict[str, Any] or JSONResponse: Masked or full response, or error response.
    """
    try:
        # Default response structure
        response = {"decision": "default", "context_used": payload.dict()}
        # Contextual logic
        if payload.user_role == "admin":
            response["decision"] = "full_access"
        elif payload.user_role == "observer":
            response["decision"] = "read_only"
        if payload.time_of_day == "after_hours":
            response["note"] = "Limited support after hours."
        if payload.agent_state == "error":
            response["decision"] = "degraded_mode"
        # Flexible return shape: field masking
        if fields:
            allowed = {f.strip() for f in fields.split(",") if f.strip()}
            filtered = {k: v for k, v in response.items() if k in allowed}
            if not filtered:
                return JSONResponse(status_code=400, content=ErrorResponse(error="No valid fields requested", detail=f"fields={fields}").dict())
            return filtered
        return response
    except ValidationError as ve:
        # Pydantic validation error
        return JSONResponse(status_code=422, content=ErrorResponse(error="Validation error", detail=str(ve)).dict())
    except Exception as e:
        # Unhandled server error
        return JSONResponse(status_code=500, content=ErrorResponse(error="Internal server error", detail=str(e)).dict())

