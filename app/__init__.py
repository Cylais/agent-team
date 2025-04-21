from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Import and include mock interface endpoints
from app.mock_interfaces import router as mock_router

app = FastAPI()
app.include_router(mock_router)

@app.get("/endpoint")
def endpoint(request: Request):
    cid = request.headers.get("X-Correlation-ID", "")
    response = JSONResponse({"status": "ok"})
    if cid:
        response.headers["X-Correlation-ID"] = cid
    return response

@app.post("/ingest")
def ingest(payload: dict):
    # Simulate ingestion logic
    return {"status": "ok", "received": payload}
