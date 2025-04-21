# Technical Architect (TA) Agent

## Overview
This agent is responsible for architectural decision-making, rationale tracking, conflict resolution, and status reporting within the autonomous agent team. It uses a Redis-backed state manager and exposes a FastAPI-based API for agent communication.

## Architecture
- **State Management:** Redis-backed decision registry, supporting distributed coordination and CRDT patterns.
- **Conflict Resolution:** Hybrid vector clock and semantic priority scoring.
- **API:** REST endpoints for decision proposal, conflict resolution, and decision status.
- **Security:** JWT validation middleware and rate limiting (see `security.py`).
- **Testing:** Contract validation and conflict simulation tests.

## Key Files
- `core.py`: State manager, decision model, conflict resolution logic
- `api.py`: FastAPI endpoints for TA agent
- `security.py`: JWT middleware
- `tests.py`: Test suite
- `__main__.py`: App entry point

## Usage
1. Ensure Redis is running and accessible (default: `localhost:6379`).
2. Install dependencies (`pip install -r requirements.txt`).
3. Run the agent: `python -m ta_agent`
4. API available at `http://localhost:8000/ta/`

## Endpoints
- `POST /ta/propose_decision`: Propose a new architecture decision
- `POST /ta/async_propose_decision`: Propose a new decision (async)
- `GET /ta/status/{decision_id}`: Get decision status
- `GET /ta/async_status/{decision_id}`: Get decision status (async)
- `GET /ta/async_list_decisions`: List all decisions (async)
- `POST /ta/async_update_decision/{decision_id}`: Update a decision (async)
- `POST /ta/async_batch_update_decisions`: Batch update decisions (async)
- `POST /ta/ai_hint`: Get AI/semantic field suggestions for decision creation
- `POST /ta/resolve_conflict`: Resolve decision conflict
- `GET /health`: Health check

## Upcoming Features
- API-wide rate limiting (FastAPI-Limiter)
- Observability: Prometheus metrics and OpenTelemetry tracing

## Testing
Run `pytest ta_agent/tests.py` to validate contract and conflict logic.

## Implementation Roadmap
- **Phase 1:** Core state management & endpoints
- **Phase 2:** Distributed conflict resolution
- **Phase 3:** Integration with other agents
