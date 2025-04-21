# Full Process for Coding with AI Coding Assistants — Adapted for agent-team

This document outlines a structured, repeatable process for your 5-agent company-style team to build production-quality software using AI-driven collaboration. Each agent has a defined role, ensuring all responsibilities are covered efficiently.

---

## 1. Team Roles & Responsibilities

| Agent Role           | Responsibilities                                                                                      |
|----------------------|------------------------------------------------------------------------------------------------------|
| Product Manager      | Oversees project, sets strategy/goals, maintains PLANNING.md & TASK.md, ensures team alignment.      |
| Tech Lead/Architect  | Designs system architecture, enforces conventions, reviews code, mentors devs, ensures modularity.    |
| Frontend Developer   | Implements user interfaces, ensures great UX, follows design & accessibility standards.               |
| Backend Developer    | Develops server logic, APIs, database, blockchain/Web3 integration, ensures security & scalability.   |
| QA Engineer/DevOps   | Tests all features, automates CI/CD, manages deployments, maintains reliability and quality.          |

---

## 2. Golden Rules (For All Agents)
- Use markdown files (`README.md`, `PLANNING.md`, `TASK.md`, `PROCESS.md`) for project management.
- Keep files under 500 lines; split into modules as needed.
- Start fresh conversations for new topics or tasks.
- One focused task per message/agent at a time.
- Test early and often; every new function should have unit tests.
- Be specific in requests, provide context and examples.
- Write docs and comments as you go; do not delay documentation.
- Manage environment variables securely; never expose secrets.

---

## 3. Project Management Artifacts

- **PLANNING.md**: Maintained by Product Manager. Contains project vision, architecture, constraints, tech stack, and tools.
- **TASK.md**: Maintained by Product Manager. Tracks current tasks, backlog, milestones, and sub-tasks.
- **PROCESS.md**: (This file) Outlines the agent-team workflow and best practices.

---

## 4. Workflow Steps

### 4.1 Planning & Task Management
- Product Manager initiates project scope in `PLANNING.md`.
- Tasks are broken down and tracked in `TASK.md`.
- All agents reference these docs before starting work.

### 4.2 Global Rules & Consistency
- Tech Lead/Architect ensures all agents follow naming conventions, file structure, and architecture patterns as described in `PLANNING.md`.

### 4.3 Modular Code & Collaboration
- Each agent works on one focused task at a time.
- Large features are split into smaller, manageable tasks.
- Agents communicate progress and blockers via markdown files and commit messages.

### 4.4 Testing & Quality Assurance
- QA/DevOps agent ensures all new features have corresponding unit tests.
- Tests are placed in a `/tests` directory.
- Mock external services in tests; cover success, failure, and edge cases.

### 4.5 Documentation
- All agents document their work as they go.
- Update `README.md` and relevant docs after each major change.

### 4.6 Deployment
- QA/DevOps agent handles Dockerization and deployment.
- Use Dockerfiles and CI/CD scripts for consistent, reproducible deployments.

---

## 5. Example Agent Workflow
1. Product Manager updates `PLANNING.md` and `TASK.md` with new feature.
2. Tech Lead reviews and refines technical approach.
3. Frontend/Backend Developers implement features in small, modular files.
4. QA/DevOps writes and runs tests, updates CI/CD, and deploys.
5. All agents update documentation and mark tasks as complete.

---

## 6. Best Practices for AI-Assisted Coding
- Always refer to `PLANNING.md` and `TASK.md` before starting a new task.
- Keep code modular and under 500 lines per file.
- Focus on one task at a time for best results.
- Test and document as you go.
- Use environment variables and never expose secrets in code.
- Use Docker for deployment; maintain a reproducible build process.

---

This process ensures your agent-team operates efficiently, with clear responsibilities, best practices, and a collaborative AI-driven workflow for building any type of full-stack or blockchain project.

---

## 7. Unified Agent-Team Roadmap Reference

All agents must refer to [`ROADMAP_UNIFIED.md`](./ROADMAP_UNIFIED.md) for the complete, up-to-date multi-agent system roadmap, including:
- Phased development plan (foundation, agent specialization, integration, platform adaptation, deployment)
- Backup & disaster recovery as a core system
- Communication protocols, tool integration, and prompt engineering
- Success metrics and learning resources

### Roadmap Summary
- **Phase 1:** Foundation & Architecture — Orchestration, agent boundaries, unified memory, robust backup system
- **Phase 2:** Agent Development — Specialized memory, prompt templates, agent capabilities
- **Phase 3:** Integration & Collaboration — Workflow orchestration, conflict resolution, feedback loops
- **Phase 4:** Platform Implementation — Web2/Web3, desktop, mobile, gaming strategies
- **Phase 5:** Deployment & Maintenance — CI/CD, monitoring, scaling, continuous improvement

**Backup system is foundational: all agent memory, project context, and state are regularly and securely backed up.**

For details, code examples, and the full summary table, see [`ROADMAP_UNIFIED.md`](./ROADMAP_UNIFIED.md).
