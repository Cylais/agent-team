# Developer (DEV) Agent

[![CI Status](https://img.shields.io/github/actions/workflow/status/RhysiiBoy/agent-team/ci.yml?branch=main)](https://github.com/RhysiiBoy/agent-team/actions/workflows/ci.yml)

## API-First, Backend-Only – See [Project Root README](../README.md) for architecture and integration context



## Overview
This agent is responsible for developer task management, assignment, conflict resolution, and status reporting within the autonomous agent team. It uses a Redis-backed state manager and exposes a FastAPI-based API for agent communication.

## Architecture
- **State Management:** Redis-backed task registry, supporting distributed coordination and CRDT patterns.
- **Conflict Resolution:** Hybrid vector clock and semantic priority scoring.
- **API:** REST endpoints for task creation, conflict resolution, and task status.
- **Security:** JWT validation middleware and rate limiting (see `security.py`).
- **Testing:** Contract validation and conflict simulation tests.

## Key Files
- `core.py`: State manager, task model, conflict resolution logic
- `api.py`: FastAPI endpoints for DEV agent
- `security.py`: JWT middleware
- `tests.py`: Test suite
- `__main__.py`: App entry point

## Usage
1. Ensure Redis is running and accessible (default: `localhost:6379`).
2. Install dependencies (`pip install -r requirements.txt`).
3. Run the agent: `python -m dev_agent`
4. API available at `http://localhost:8000/dev/`

## Redis Connection Pool Configuration

The DEV agent supports fine-tuned Redis connection pool settings via environment variables. All parameters are validated and defaults are provided for robust operation:

| Variable                                 | Type    | Default                  | Description / Range                  |
|------------------------------------------|---------|--------------------------|--------------------------------------|
| DEV_AGENT_REDIS_URL                      | str     | redis://localhost:6379   | Redis server URL                     |
| DEV_AGENT_REDIS_MAX_CONNECTIONS          | int     | 100                      | Max pool connections (1-1000)        |
| DEV_AGENT_REDIS_SOCKET_KEEPALIVE         | bool    | True                     | Enable TCP keepalive                 |
| DEV_AGENT_REDIS_RETRY_ON_TIMEOUT         | bool    | True                     | Retry on timeout                     |
| DEV_AGENT_REDIS_SOCKET_CONNECT_TIMEOUT   | float   | 3                        | Socket connect timeout (seconds)     |
| DEV_AGENT_REDIS_SOCKET_TIMEOUT           | float   | 5                        | Socket operation timeout (seconds)   |

Example:
```bash
export DEV_AGENT_REDIS_MAX_CONNECTIONS=200
export DEV_AGENT_REDIS_SOCKET_KEEPALIVE=False
```

All settings are logged at startup for observability.

## Endpoints
- `POST /dev/create_task`: Create a new developer task
- `GET /dev/status/{task_id}`: Get task status
- `POST /dev/resolve_conflict`: Resolve task conflict
- `GET /health`: Health check

## Testing
Run `pytest dev_agent/tests.py` to validate contract and conflict logic.

## Implementation Roadmap
- **Phase 1:** Core state management & endpoints
- **Phase 2:** Distributed conflict resolution
- **Phase 3:** Integration with other agents
