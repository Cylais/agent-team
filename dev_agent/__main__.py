from fastapi import FastAPI
from dev_agent.api import dev_router
from dev_agent.security import validate_jwt
from dev_agent.rate_limit import init_rate_limiter
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from dev_agent.metrics import update_redis_circuit_metric
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
import os

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI Limiter, Prometheus metrics, and OpenTelemetry tracing on startup.
    Tracing is exported via OTLP to the endpoint specified by OTEL_EXPORTER_OTLP_ENDPOINT (default: http://localhost:4318/v1/traces).
    """
    import asyncio
    await init_rate_limiter(app)
    Instrumentator().instrument(app).expose(app)
    # Schedule Redis circuit breaker metric update
    async def update_metric_periodically():
        while True:
            update_redis_circuit_metric()
            await asyncio.sleep(5)
    asyncio.create_task(update_metric_periodically())
    # OpenTelemetry tracing setup
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
    tracer_provider = TracerProvider()
    span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

app.include_router(dev_router)

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
