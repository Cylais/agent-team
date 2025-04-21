# Agent-Team: Autonomous Multi-Agent Backend System

[![CI Status](https://img.shields.io/github/actions/workflow/status/RhysiiBoy/agent-team/ci.yml?branch=main)](https://github.com/RhysiiBoy/agent-team/actions/workflows/ci.yml)

## Enterprise-Grade, API-First, Backend-Only

## Overview

This project implements a robust, modular, and fully autonomous multi-agent development team. It is designed for API-first, backend-only operation—**no frontend, onboarding UI, or platform UI are in scope**. The system is architected for integration, extensibility, and rigorous testing, as detailed in [`ROADMAP_UNIFIED.md`](./ROADMAP_UNIFIED.md) and [`project_architecture.md`](./project_architecture.md).

## Key Features & Scope

- **API-First**: All interactions are via documented HTTP APIs (see `app/` and `api/`).
- **Modular Agents**: Five specialized agents (PM, TA, DEV, QA, UX), each with distinct roles and memory models.
- **Orchestration Layer**: Central workflow and agent registration via Windsurf (Cascade).
- **Unified Memory**: Vector DB-backed context layer (short-term, episodic, semantic, procedural).
- **Event-Driven Messaging**: Standardized JSON/Protobuf protocols, async/sync channels, and message prioritization.
- **Backup & Disaster Recovery**: Automated, versioned backups and recovery playbooks.
- **Observability & Tooling**: Integrated Prometheus metrics, OpenTelemetry tracing, and a tool registry.
- **Testing**: Comprehensive unit, integration, property-based, and chaos tests.

## Project Structure

- `app/`: FastAPI app, API endpoints, and event handlers
- `agents/`, `api/`: Core agent logic and API contracts
- `scripts/`: ML pipelines, merge drivers, and utilities
- `config/`: Feature flags and environment config
- `tests/`: All test suites (`unit/`, `integration/`, `property_based/`, `legacy/`)
- `docs/`: Architecture, protocol, and onboarding docs
- `.github/workflows/`: CI/CD, chaos engineering, and validation pipelines

## Agent Roles

- **PM Agent**: Project management, coordination, and escalation
- **TA Agent**: Technical architecture, design, and review
- **DEV Agent**: Implementation, code generation, and refactoring
- **QA Agent**: Testing, validation, and chaos engineering
- **UX Agent**: Usability, accessibility, and user-centric feedback

See [`agent_roles_foundation.md`](./agent_roles_foundation.md) for detailed descriptions and boundaries.

## Getting Started

1. **Clone the Repo**

   ```bash
   git clone https://github.com/Cylais/agent-team.git
   cd agent-team
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API Server**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run Tests**

   ```bash
   pytest tests/
   ```

## Integration & Extension

- **API Reference**: See OpenAPI/Swagger docs at `/docs` when server is running
- **Custom Agents/Tools**: Extend via `agents/` and `tool_registry.py`
- **Message Protocols**: See [`agent_communication_protocol.md`](./agent_communication_protocol.md)
- **Backup/Restore**: See [`backup_system_schema.sql`](./backup_system_schema.sql) and disaster recovery docs

## Contribution Guidelines

- Follow the architecture and process docs in `docs/`
- All changes must pass CI and all tests
- Update the roadmap and checklist as appropriate
- Document major decisions in `decisions.md`

## References

- [ROADMAP_UNIFIED.md](./ROADMAP_UNIFIED.md): Project roadmap and milestones
- [CHECKLIST.md](./CHECKLIST.md): Active and completed tasks
- [project_architecture.md](./project_architecture.md): System architecture
- [session_log.md](./session_log.md): Progress and session history

## Status

- **Phase 1**: Complete
- **Phase 2**: Individual agent implementation and integration in progress

See the roadmap for current priorities and next steps.

---

## License

[MIT](./LICENSE) (or as specified)
