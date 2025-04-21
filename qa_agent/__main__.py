from fastapi import FastAPI
from qa_agent.api import qa_router
from qa_agent.security import validate_jwt
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from .rate_limit import setup_rate_limiter
import asyncio

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await setup_rate_limiter(app)

app.include_router(qa_router)

# Prometheus metrics
request_counter = Counter("qa_requests_total", "Total QA API requests")

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    request_counter.inc()
    return response

@app.get("/qa/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}
