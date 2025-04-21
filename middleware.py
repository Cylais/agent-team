"""
FastAPI Middleware for Correlation ID Propagation with OpenTelemetry Compatibility
- Extracts or generates a correlation ID per request
- Stores correlation ID in request context for logging
- Injects correlation ID into outgoing response headers
- Compatible with OpenTelemetry W3C Trace Context
"""
from uuid import uuid4
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry.propagate import inject, extract

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract or generate correlation ID
        headers = dict(request.headers)
        ctx = extract(headers)
        correlation_id = ctx.get("x-correlation-id") or str(uuid4())
        request.state.correlation_id = correlation_id
        # Inject into outgoing headers
        response: Response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        inject({"x-correlation-id": correlation_id}, response.headers)
        return response

# Usage (in FastAPI app):
# from middleware import CorrelationIdMiddleware
# app.add_middleware(CorrelationIdMiddleware)
