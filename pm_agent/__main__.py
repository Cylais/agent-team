from fastapi import FastAPI
from pm_agent.api import pm_router, prometheus_instrumentator, pm_state
from pm_agent.rate_limit import init_rate_limiter
from pm_agent.security import validate_jwt
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import asyncio

app = FastAPI()

# Instrument Prometheus
prometheus_instrumentator.instrument(app).expose(app)

# Instrument OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

app.include_router(pm_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Start background circuit breaker monitor
    asyncio.create_task(pm_state.circuit_breaker_monitor())
    # Initialize FastAPI-Limiter for rate limiting
    await init_rate_limiter(app)


@app.get("/health")
async def health():
    return {"status": "ok"}
