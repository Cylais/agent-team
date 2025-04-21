from fastapi import FastAPI
from ta_agent.api import ta_router
from ta_agent.security import validate_jwt
from fastapi.middleware.cors import CORSMiddleware
from ta_agent.rate_limit import setup_rate_limiter
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await setup_rate_limiter(app)

app.include_router(ta_router)

# Prometheus metrics
REQUEST_COUNTER = Counter('ta_agent_requests_total', 'Total requests to TA agent')

@app.middleware('http')
async def count_requests(request, call_next):
    response = await call_next(request)
    REQUEST_COUNTER.inc()
    return response

@app.get('/ta/metrics')
def metrics():
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
