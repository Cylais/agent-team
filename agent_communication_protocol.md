# Agent Communication Protocol

## Overview
This document defines the message serialization, error handling, versioning, and integration requirements for the Dev-Agent system. It is intended to ensure API-first, robust, and testable communication between agents and external systems.

---

## Message Serialization
- All API payloads MUST be JSON-encoded.
- Timestamps use ISO 8601 format.
- All task, status, and conflict messages follow the schemas defined in the OpenAPI spec (`api.py` models).
- Non-breaking schema changes are versioned via additive fields; breaking changes require a new API version.

## Error Handling
- All errors are returned as JSON objects with at least `error` and `detail` fields.
- HTTP status codes are used according to REST conventions (e.g., 400 for validation, 404 for not found, 500 for internal errors).
- Circuit breaker and rate limit errors return 429 or 503 with clear `error` messages.

## Versioning
- The API version is specified via the URL path prefix (e.g., `/v1/dev/...`).
- Major breaking changes increment the version; minor/patch changes are backward compatible.
- Clients are expected to check the version and adapt accordingly.

## Integration & Testing
- Mock/test endpoints are provided for integration readiness (see `/dev/test/*`).
- Contract testing (e.g., Pact) is required for all third-party and cross-agent integrations.
- All endpoints are covered by behavioral and regression tests in `tests/`.

## Out of Scope
- No frontend, onboarding, or UI logic is handled by this protocol.
- All communication is strictly via documented RESTful endpoints.

---

For further details, see `project_architecture.md`, `ROADMAP_UNIFIED.md`, and the OpenAPI documentation in `api.py`.
