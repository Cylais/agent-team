# Project Manager (PM) Agent

[![CI Status](https://img.shields.io/github/actions/workflow/status/RhysiiBoy/agent-team/ci.yml?branch=main)](https://github.com/RhysiiBoy/agent-team/actions/workflows/ci.yml)

## API-First, Backend-Only – See [Project Root README](../README.md) for architecture and integration context


## Overview
This agent is responsible for project coordination, task assignment, conflict resolution, and status reporting within the autonomous agent team. It uses a Redis-backed state manager and exposes a FastAPI-based API for agent communication.

## Architecture

- **State Management:** Redis-backed task registry (async, circuit breaker protected), supporting distributed coordination and CRDT patterns.
- **Conflict Resolution:** Hybrid vector clock, semantic similarity, and priority scoring (see `batch_ai_semantic.py`).
- **Batch Operations:** Async batch update with Redis pipelining for efficient bulk task changes.
- **AI/Semantic Hints:** Automatic task field suggestions using ML (see `batch_ai_semantic.py`).
- **Rate Limiting:** API-wide rate limiting using FastAPI-Limiter and Redis.
- **Contract Testing:** Pact contract test stub included.
- **API:** REST endpoints for task assignment, conflict resolution, and task status (all async, JWT-protected).
- **Observability:** Prometheus metrics (`/pm/metrics`), OpenTelemetry distributed tracing, logging, and background circuit breaker monitor.
- **Security:** JWT validation middleware and rate limiting (see `security.py`).
- **Testing:** Contract validation and conflict simulation tests.

## Key Files

- `core.py`: State manager, task model, conflict resolution logic
- `batch_ai_semantic.py`: Batch updates, AI/semantic hints, semantic conflict resolution
- `api.py`: FastAPI endpoints for PM agent
- `security.py`: JWT middleware
- `rate_limit.py`: FastAPI-Limiter setup for API rate limiting
- `contract_test_pact.py`: Pact contract test stub
- `tests.py`: Test suite
- `__main__.py`: App entry point

## Usage

1. Ensure Redis is running and accessible (default: `localhost:6379`).
2. Install dependencies (`pip install -r requirements.txt`).
   - Requires `fastapi-limiter`, `scikit-learn`, and `redis[asyncio]` for full feature support.
3. Run the agent: `python -m pm_agent`
4. API available at `http://localhost:8000/pm/`
5. Prometheus metrics at `http://localhost:8000/pm/metrics`
6. Distributed tracing (OpenTelemetry) auto-instrumented for all endpoints (see your tracing backend).
7. Circuit breaker monitor runs in the background and will log/metric Redis outages.

## Endpoints

- `POST /pm/assign_task`: Assign a new task (async, JWT + rate limit)
- `GET /pm/status/{task_id}`: Get task status (async, JWT + rate limit)
- `POST /pm/resolve_conflict`: Resolve task conflict using semantic/ML logic (JWT + rate limit)
- `POST /pm/batch_update`: Batch update tasks (async, JWT + rate limit)
- `POST /pm/ai_hint`: Get AI/semantic field suggestions for task creation (JWT + rate limit)
- `GET /pm/metrics`: Prometheus metrics scrape endpoint
- `GET /health`: Health check

## Testing

Run `pytest pm_agent/tests.py` to validate contract and conflict logic.

## Implementation Roadmap

- **Phase 1:** Core state management & endpoints
- **Phase 2:** Distributed conflict resolution
- **Phase 3:** Integration with other agents
