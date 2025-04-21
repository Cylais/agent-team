# Project Architecture: Distributed Validation, Observability & Conflict Resolution

## Agent Roles, Boundaries & Responsibilities

### PM Agent (Project Manager)
- **Role:** Orchestrates project planning, sprint management, and task assignment across all agents.
- **Boundaries:** No direct code execution or task implementation; only coordinates via API.
- **Responsibilities:**
  - Create, update, and close sprints
  - Assign tasks to agents
  - Track progress and generate reports
  - Integrate with Dev-Agent, QA-Agent, TA-Agent, and UX-Agent via REST endpoints
- **Key Protocols:**
  - Task assignment and status update schema
  - Sprint planning endpoints

### TA Agent (Tech Architect)
- **Role:** Manages architectural decisions, technical standards, and reviews implementation proposals.
- **Boundaries:** No direct project management or QA; only provides architecture guidance and reviews.
- **Responsibilities:**
  - Propose, review, and approve architecture changes
  - Maintain architecture documentation
  - Validate compliance with standards
- **Key Protocols:**
  - Architecture proposal/review endpoints
  - Standard compliance reporting

### QA Agent (Quality Assurance)
- **Role:** Handles automated and manual QA, test orchestration, and test result reporting.
- **Boundaries:** No direct feature implementation; only tests and validates outputs from other agents.
- **Responsibilities:**
  - Run and manage test suites
  - Report defects and regression issues
  - Validate contract and integration compliance
- **Key Protocols:**
  - Test orchestration endpoints
  - Defect reporting schema

### UX Agent (User Experience)
- **Role:** Provides UX review, feedback, and design guidance for APIs and developer-facing features.
- **Boundaries:** No direct implementation or project management; only reviews and suggests improvements.
- **Responsibilities:**
  - Review API usability and documentation
  - Suggest improvements to developer experience
  - Maintain UX best practices documentation
- **Key Protocols:**
  - UX review endpoints
  - Feedback/comment schema

## System Boundaries & API-First Scope
- The Dev-Agent system is strictly API-first: all features, integrations, and agent interactions are exposed via RESTful endpoints.
- All frontend, onboarding, and platform UI are explicitly out of scope for this repository.
- The system boundary is defined at the API contract; all communication, state management, and orchestration occur via documented endpoints.
- Protocols for message serialization, error handling, and versioning are specified in `agent_communication_protocol.md` (see also: `ROADMAP_UNIFIED.md`).
- Integration readiness is ensured through mock/test interfaces and contract testing (see checklist).

## Parallel Test Strategy
- All legacy test suites preserved in `tests/legacy/`
- Property-based and chaos-driven tests in `tests/property_based/`
- Both tracks run in CI for regression and edge-case coverage

## Merge Conflict Resolution
- `.gitattributes` uses semantic merge driver for schema files
- `scripts/merge_schema` performs JSONPath-aware merges
- ML pipeline (`ml_conflict_prediction.py`) predicts likely conflicts before merge

## Observability & Feature Flags
- Prometheus alerting controlled via `config/feature_flags.yml`
- Tiered alerting for circuit breaker, trace completeness
- All new metrics/alerts rolled out behind feature flags for safe adoption

## Chaos Engineering
- CI/CD workflows inject Redis latency, Postgres failover, network partitions
- Advanced chaos: Byzantine fault injection via `chaos_byzantine.yml`
- Trace completeness validated post-chaos with Jaeger/OTel integration

## Documentation & Governance
- All architecture, test, and chaos patterns documented here and in `session_log.md`
- Update this file with every major integration or workflow change
