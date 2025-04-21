# Agent Boundaries and Responsibilities

## Overview
This document details the explicit boundaries (what each agent is responsible for and what is out of scope) for the five core agents, ensuring clear separation of concerns and adherence to system boundaries as defined in the roadmap and project architecture.

---

## 1. Project Manager (PM)
**In Scope:**
- Task decomposition, assignment, and progress tracking
- Inter-agent dependency management
- Escalation of blockers and coordination of fallback/escalation
**Out of Scope:**
- Direct implementation of features or tests
- Technical architecture decisions (delegated to TA)
- User experience review (delegated to UX)

## 2. Technical Architect (TA)
**In Scope:**
- System architecture and technical standards
- API/interface review and approval
- Guidance on scalability, integration, and technical risk
**Out of Scope:**
- Project management and task assignment
- Feature implementation (delegated to DEV)
- Quality assurance and usability review

## 3. Developer (DEV)
**In Scope:**
- Implementation of features and bug fixes
- Writing and running unit/integration tests
- Requesting technical clarification from TA
**Out of Scope:**
- Defining project scope or architecture
- Task assignment (handled by PM)
- Final QA or usability review

## 4. Quality Assurance (QA)
**In Scope:**
- Test plan design and execution
- Defect reporting and verification
- System health and compliance monitoring
**Out of Scope:**
- Feature implementation or architecture
- Task assignment
- UX review (delegated to UX)

## 5. User Experience (UX)
**In Scope:**
- Usability review of features and agent interactions
- API ergonomics suggestions
- Documentation of user-facing API behaviors
**Out of Scope:**
- Project management and technical architecture
- Feature implementation or test execution
- Task assignment

---

## Next Steps
- Review these boundaries with reference to the roadmap and architecture docs.
- Iterate as needed and finalize in the main project documentation.
