# User Experience (UX) Agent

## Overview
This agent is responsible for user experience feedback management, assignment, conflict resolution, and status reporting within the autonomous agent team. It uses a Redis-backed state manager and exposes a FastAPI-based API for agent communication.

## Architecture
- **State Management:** Redis-backed feedback registry, supporting distributed coordination and CRDT patterns.
- **Conflict Resolution:** Hybrid vector clock and semantic priority scoring.
- **API:** REST endpoints for feedback creation, conflict resolution, and feedback status.
- **Security:** JWT validation middleware and rate limiting (see `security.py`).
- **Testing:** Contract validation and conflict simulation tests.

## Key Files
- `core.py`: State manager, feedback model, conflict resolution logic
- `api.py`: FastAPI endpoints for UX agent
- `security.py`: JWT middleware
- `tests.py`: Test suite
- `__main__.py`: App entry point

## Usage
1. Ensure Redis is running and accessible (default: `localhost:6379`).
2. Install dependencies (`pip install -r requirements.txt`).
3. Run the agent: `python -m ux_agent`
4. API available at `http://localhost:8000/ux/`

## Endpoints
- `POST /ux/create_feedback`: Create a new UX feedback item
- `GET /ux/status/{feedback_id}`: Get feedback status
- `POST /ux/resolve_conflict`: Resolve feedback conflict
- `GET /health`: Health check

## Testing
Run `pytest ux_agent/tests.py` to validate contract and conflict logic.

## Implementation Roadmap
- **Phase 1:** Core state management & endpoints
- **Phase 2:** Distributed conflict resolution
- **Phase 3:** Integration with other agents
