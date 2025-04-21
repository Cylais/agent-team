# Project Architecture

## System Boundaries
- **In Scope:** Agent coordination logic, instruction processing pipelines, inter-agent APIs
- **Out of Scope:** User-facing interfaces, session persistence, deployment orchestration, onboarding, dashboards, billing, etc.

## API Layer Specifications
| API Type              | Purpose                        | Standards         |
|-----------------------|--------------------------------|-------------------|
| Instruction Ingestion | Receive project specs from UI  | REST/WebSocket    |
| Status Reporting      | Push build progress updates    | SSE/Webhook       |
| Control Interface     | Accept runtime directives      | gRPC              |

## Documentation Strategy
- Protocol specifications are maintained in agent_communication_protocol.md
- Mock interfaces and integration tests are required for all external APIs
- All boundaries and exclusions are reviewed at each roadmap milestone

## Integration Milestones
- Agent<->Platform Event Bus (Q3 2025)
- WebSocket Control Channel Spec (Q4 2025)
- API Layer Stress Test (Q1 2026)
