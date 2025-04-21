from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

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
