# Agent Communication Protocol

## Overview
Defines the message formats, API contracts, orchestration logic, fallback/escalation paths, and monitoring hooks for agent-to-agent and agent-to-orchestrator communication.

---

## Message Format (JSON Schema)

| Field           | Type     | Description                                                      |
|-----------------|----------|------------------------------------------------------------------|
| sender          | string   | Role of the sending agent (e.g., "DEV", "QA")                   |
| recipient       | string   | Role of the receiving agent                                      |
| type            | string   | Message type: task, status, query, escalation, feedback          |
| correlation_id  | string   | Unique ID to correlate request/response chains                   |
| timestamp       | string   | ISO8601 UTC timestamp                                            |

```json
{
  "sender": "agent_role",
  "recipient": "agent_role",
  "type": "task|status|query|escalation|feedback",
  "correlation_id": "string",
  "timestamp": "ISO8601 string",
  "payload": { "...": "..." },
  "priority": "low|normal|high|urgent",
  "metadata": { "...": "..." }
}
```

### Example Payloads
- **Task:**
```json
{
  "sender": "PM",
  "recipient": "DEV",
  "type": "task",
  "correlation_id": "task-001",
  "timestamp": "2025-04-21T09:00:00Z",
  "payload": { "feature": "user login", "deadline": "2025-04-25" },
  "priority": "high",
  "metadata": { "sprint": "Q2-1" }
}
```
- **Escalation:**
```json
{
  "sender": "DEV",
  "recipient": "PM",
  "type": "escalation",
  "correlation_id": "bug-1034",
  "timestamp": "2025-04-21T11:30:00Z",
  "payload": { "issue": "Unclear requirements for feature X" },
  "priority": "urgent",
  "metadata": { "blocker": true }
}
```
- **Status:**
```json
{
  "sender": "QA",
  "recipient": "PM",
  "type": "status",
  "correlation_id": "test-2025-04-21",
  "timestamp": "2025-04-21T13:00:00Z",
  "payload": { "tests_passed": 98, "tests_failed": 2 },
  "priority": "normal",
  "metadata": { "build": "v1.2.3" }
}
```

---

## Message Flow Diagram

```
PM/TA/UX
   |
   v
 Orchestrator <--> DEV <--> QA
   ^                    ^
   |                    |
  Stakeholders       Feedback
```
- Messages are routed through the orchestrator for delivery, monitoring, and escalation.
- Escalations and feedback can flow in both directions.

---

## API Contracts
- All messages must conform to the above schema.
- **Endpoints:**
  - `/agent/send` for agent-to-agent messages
  - `/agent/escalate` for escalation paths
  - `/agent/status` for status and health checks
- **Versioning:** All contracts are versioned and backward compatible.

---

## Protocol Specifications
- **Message Serialization:** All inter-agent and external messages use Protocol Buffers (preferred) or JSON schema. Example schemas and versioning strategies included below.

### Protocol Buffers Example
```protobuf
syntax = "proto3";
package agent;

message AgentMessage {
  string sender = 1;
  string recipient = 2;
  string type = 3; // task, status, query, escalation, feedback
  string correlation_id = 4;
  string timestamp = 5;
  string priority = 6; // low, normal, high, urgent
  map<string, string> metadata = 7;
  bytes payload = 8; // serialized JSON or binary
}
```

- **Error Handling:** Standardized error codes, retry/fallback, and escalation workflows for failed agent interactions. See error handling workflow diagrams.
- **Versioning:** API endpoints and message schemas use semantic versioning (MAJOR.MINOR.PATCH). Breaking changes increment MAJOR, backward-compatible changes increment MINOR, PATCH for bugfixes. All changes are documented and migration steps provided for breaking changes.
- **Mock Interfaces:**
    - Instruction payload schema (JSON template)
    - Build status webhook endpoint
    - Session control endpoints (start/pause/terminate)
    - [See checklist for implementation tracking]
- **Integration Readiness:**
    - 99.9% message delivery reliability
    - <500ms round-trip latency for control signals
    - Graceful degradation under 10k concurrent sessions
- **Message Serialization:** All inter-agent and external messages use Protocol Buffers (preferred) or JSON schema. Example schemas and versioning strategies included below.
- **Error Handling:** Standardized error codes, retry/fallback, and escalation workflows for failed agent interactions. See error handling workflow diagrams.
- **Versioning:** API endpoints and message schemas are versioned using semantic versioning. Breaking changes require explicit migration steps.
- **Mock Interfaces:**
    - Instruction payload schema (JSON template)
    - Build status webhook endpoint
    - Session control endpoints (start/pause/terminate)
- **Integration Readiness:**
    - 99.9% message delivery reliability
    - <500ms round-trip latency for control signals
    - Graceful degradation under 10k concurrent sessions

## Orchestration Layer
- Handles routing, delivery guarantees, and retries.
- Monitors message status and triggers fallback if no response within timeout.
- Logs all communication for audit and improvement cycles.

---

## Fallback & Escalation

- If an agent fails to respond or resolve a task, the orchestrator escalates to the next responsible agent (as per agent_roles_and_boundaries.md).
- Escalation is logged and triggers stakeholder notification if unresolved.

### Error Handling

- Malformed messages are rejected with a detailed error response (`400 Bad Request`).
- Contract violations trigger a protocol error log and alert the sender.
- All errors are tracked and reviewed in retrospectives.

---

## Monitoring & Feedback

- Real-time tracking of message delivery and processing status
- Feedback loops: agents acknowledge receipt, provide status updates, and flag errors
- Monitoring hooks for escalation and contract violations
- Dashboard visualizes message flow, escalation frequency, and SLA adherence
- Automated alerts for dropped/malformed messages or missed SLAs

---

## Error Handling

- Malformed messages are rejected with error details sent to sender
- Contract violations are logged and escalated to PM/TA
- Retries and fallback protocols for undelivered messages

---

## Changelog

- **2025-04-21:** Clarified schema, added examples, diagrams, error handling, and changelog.
