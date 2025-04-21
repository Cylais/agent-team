# Quality Assurance (QA) Agent

## Overview
This agent is responsible for quality assurance test case management, assignment, conflict resolution, and status reporting within the autonomous agent team. It uses a Redis-backed state manager and exposes a FastAPI-based API for agent communication.

## Architecture
- **State Management:** Redis-backed test registry, supporting distributed coordination and CRDT patterns.
- **Conflict Resolution:** Hybrid vector clock and semantic priority scoring.
- **API:** REST endpoints for test case creation, conflict resolution, and test status.
- **Security:** JWT validation middleware and rate limiting (see `security.py`).
- **Testing:** Contract validation and conflict simulation tests.

## Key Files
- `core.py`: State manager, test case model, conflict resolution logic
- `api.py`: FastAPI endpoints for QA agent
- `security.py`: JWT middleware
- `tests.py`: Test suite
- `__main__.py`: App entry point

## Usage
1. Ensure Redis is running and accessible (default: `localhost:6379`).
2. Install dependencies (`pip install -r requirements.txt`).
3. Run the agent: `python -m qa_agent`
4. API available at `http://localhost:8000/qa/`

## Endpoints
- `POST /qa/create_test`: Create a new QA test case
- `GET /qa/status/{test_id}`: Get test status
- `POST /qa/resolve_conflict`: Resolve test conflict
- `GET /health`: Health check

## Testing
Run `pytest qa_agent/tests.py` to validate contract and conflict logic.

## Implementation Roadmap
- **Phase 1:** Core state management & endpoints
- **Phase 2:** Distributed conflict resolution
- **Phase 3:** Integration with other agents
