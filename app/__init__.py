from fastapi import FastAPI

app = FastAPI()

@app.post("/ingest")
def ingest(payload: dict):
    # Simulate ingestion logic
    return {"status": "ok", "received": payload}
