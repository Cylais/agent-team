# Agent-Team

This project implements a multi-agent autonomous development team as described in the ROADMAP_UNIFIED.md. See the roadmap and process documents for architecture and implementation details.

## Project Structure (2025-04)

- `app/`: FastAPI app and event handlers
- `agents/`, `api/`, etc.: Core modules
- `scripts/`: ML pipeline, merge drivers, utility scripts
- `config/`: Feature flags, configuration
- `tests/`
    - `unit/`: Unit tests for core logic
    - `integration/`: Integration tests (multi-component, DB, service)
    - `property_based/`: Property-based and chaos tests
    - `legacy/`: Legacy tests
- `docs/`: Documentation and onboarding
- `.github/workflows/`: CI/CD and chaos workflows

All tests are run via `pytest tests/` or by specifying a subfolder.
