# Agent Roles & Boundaries: Phase 2A Draft

## 1. Project Manager (PM)
- Coordinates all agent activities, sets priorities, and resolves conflicts
- Owns the overall project timeline, deliverables, and quality gates
- Interfaces with stakeholders (simulated/external)
- API: `/pm/assign_task`, `/pm/resolve_conflict`, `/pm/status`

## 2. Technical Architect (TA)
- Defines technical standards, architecture, and integration patterns
- Reviews all proposed changes for compliance
- API: `/ta/review_design`, `/ta/approve_architecture`, `/ta/status`

## 3. Developer (DEV)
- Implements features, fixes bugs, and writes tests
- Responds to task assignments and code reviews
- API: `/dev/submit_code`, `/dev/respond_review`, `/dev/status`

## 4. Quality Assurance (QA)
- Designs and executes test plans, validates deliverables
- Flags regressions and verifies bug fixes
- API: `/qa/submit_report`, `/qa/flag_issue`, `/qa/status`

## 5. User Experience (UX)
- Reviews usability, accessibility, and user feedback
- Proposes improvements to workflow and UI (for simulation, not real UI)
- API: `/ux/submit_feedback`, `/ux/propose_change`, `/ux/status`

---

# Standardized Communication Protocols (Draft)

- **Message Format:**
  - JSON/Protobuf with fields: `sender`, `recipient`, `type`, `content`, `metadata`, `priority`
- **API Contracts:**
  - Each agent exposes REST endpoints for its role-specific actions
  - All endpoints accept/return standardized message objects
- **Error Handling:**
  - Structured error schema: `error_code`, `message`, `details`, `next_steps`
- **Versioning:**
  - All APIs versioned via `/v1/`, `/v2/`, etc.
- **Authentication:**
  - JWT or mTLS enforced for all endpoints

---

*This draft is aligned with the Phase 2A roadmap and will be iterated as development progresses.*
