# Agent-Team: Autonomous Multi-Agent Backend System

[![CI Status](https://img.shields.io/github/actions/workflow/status/RhysiiBoy/agent-team/ci.yml?branch=main)](https://github.com/RhysiiBoy/agent-team/actions/workflows/ci.yml)

## Enterprise-Grade, API-First, Backend-Only

---

## Overview

This project implements a robust, modular, and fully autonomous multi-agent development team. See [`ROADMAP_UNIFIED.md`](./ROADMAP_UNIFIED.md) and [`project_architecture.md`](./project_architecture.md) for details. **No frontend, onboarding UI, or platform UI are in scope.**

---

## Key Features & Scope

- **API-First**: All interactions via documented HTTP APIs (`app/`, `api/`)
- **Modular Agents**: PM, TA, DEV, QA, UX—distinct roles and memory models
- **Orchestration Layer**: Central workflow and agent registration via Windsurf (Cascade)
- **Unified Memory**: Vector DB-backed context
- **Event-Driven Messaging**: JSON/Protobuf protocols, async/sync channels
- **Backup & Recovery**: Automated, versioned backups
- **Observability**: Prometheus metrics, OpenTelemetry tracing
- **Testing**: Unit, integration, property-based, chaos tests

---

## Project Structure

- `app/`: FastAPI app, API endpoints, event handlers
- `agents/`, `api/`: Core agent logic and API contracts
- `scripts/`: ML pipelines, merge drivers, utilities
- `config/`: Feature flags, environment config
- `tests/`: All test suites (`unit/`, `integration/`, `property_based/`, `legacy/`)
- `docs/`: Architecture, protocol, onboarding docs
- `.github/workflows/`: CI/CD, chaos engineering, validation pipelines

---

## Agent Roles

- **PM Agent**: Project management, coordination, escalation
- **TA Agent**: Technical architecture, design, review
- **DEV Agent**: Implementation, code generation, refactoring
- **QA Agent**: Testing, validation, chaos engineering
- **UX Agent**: Usability, accessibility, user-centric feedback

See [`agent_roles_foundation.md`](./agent_roles_foundation.md) for details.

---

## Getting Started

1. **Clone the Repo**

   ```bash
   git clone https://github.com/RhysiiBoy/agent-team.git
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

---

## Contribution Guidelines

- Follow docs in `docs/`
- All changes must pass CI and all tests
- Update roadmap and checklist as appropriate
- Document major decisions in `decisions.md`

---

## References

- [ROADMAP_UNIFIED.md](./ROADMAP_UNIFIED.md)
- [CHECKLIST.md](./CHECKLIST.md)
- [project_architecture.md](./project_architecture.md)
- [session_log.md](./session_log.md)

---

## Status

- **Phase 1**: Complete
- **Phase 2**: Agent implementation and integration in progress

See roadmap for current priorities and next steps.

---

## License

[MIT](./LICENSE) (or as specified)
