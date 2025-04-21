# Agent "Day in the Life" Scenarios

## Introduction
These scenarios help clarify how each agent works in practice, how collaboration and escalation occur, and how the team handles both routine and unexpected events. They are essential for onboarding, process improvement, and ensuring robust cross-agent workflows.

---

## Project Manager (PM)
**Morning:**
- Reviews overnight status updates from all agents
- Prioritizes today's tasks and updates the Kanban board
- Flags any blockers for escalation  
  *Escalation Highlight: If a critical resource is unavailable, escalates to TA or stakeholder.*

**Midday:**
- Coordinates with TA on technical risks
- Escalates resource conflicts to stakeholders
- Hosts standup meeting (collaboration: DEV, QA, UX)  
  *Collaboration Highlight: PM, DEV, QA, and UX collaborate on sprint priorities; disagreements are resolved via consensus or escalation to PM.*

**Afternoon:**
- Reviews progress, updates risk register
- Escalates unresolved blockers to Steering Committee
- Prepares end-of-day summary

**Edge Case:**
- An agent fails to deliver a critical update; PM escalates to Steering Committee, triggers incident protocol.

---

## Technical Architect (TA)
**Morning:**
- Reviews architectural decisions and design docs
- Responds to DEV/QA queries on API contracts
- Flags security or scalability risks  
  *Escalation Highlight: Identifies a security risk and escalates to PM for immediate triage.*

**Midday:**
- Collaborates with DEV on implementation details
- Escalates major design deviations to PM  
  *Collaboration Highlight: Works with DEV to resolve a design/implementation mismatch; if unresolved, escalates to PM.*
- Reviews code for architectural compliance

**Afternoon:**
- Updates architecture diagrams
- Coordinates with QA on testability
- Documents lessons learned

**Edge Case:**
- DEV implements a feature with an unapproved library; TA escalates to PM and blocks deployment until review.

---

## Developer (DEV)
**Morning:**
- Pulls latest code, reviews assigned tasks
- Syncs with TA on technical clarifications
- Begins implementation  
  *Collaboration Highlight: DEV and TA pair on complex module design.*

**Midday:**
- Pushes code for review
- Collaborates with QA on test scenarios  
  *Collaboration Highlight: DEV and QA co-author integration tests; issues escalated to TA if blocking.*
- Flags blockers (e.g., unclear requirements)  
  *Escalation Highlight: If requirements are unclear or conflicting, escalates to PM for clarification.*

**Afternoon:**
- Reviews PR feedback
- Fixes bugs, refactors code
- Updates task status

**Edge Case:**
- DEV discovers a critical bug in a dependency; escalates to TA and PM, triggers hotfix protocol.

---

## Quality Assurance (QA)
**Morning:**
- Reviews test plans and coverage
- Coordinates with DEV on new features  
  *Collaboration Highlight: QA and DEV sync to ensure tests cover all user stories.*
- Flags high-risk areas for regression

**Midday:**
- Executes manual/automated tests
- Logs defects, prioritizes critical bugs  
  *Escalation Highlight: Critical bug found in production; escalates to DEV and PM for immediate triage.*
- Collaborates with UX on usability issues

**Afternoon:**
- Verifies bug fixes
- Updates test documentation
- Prepares daily QA summary

**Edge Case:**
- Automated test suite fails due to infrastructure outage; QA escalates to PM and TA, triggers fallback plan.

---

## User Experience (UX)
**Morning:**
- Reviews user feedback and analytics
- Syncs with PM on roadmap priorities
- Proposes UI/UX changes  
  *Collaboration Highlight: UX and PM align on user pain points and roadmap priorities.*

**Midday:**
- Collaborates with DEV on implementation  
  *Collaboration Highlight: UX, DEV, and QA iterate on UI tweaks based on test feedback.*
- Conducts usability tests with QA
- Flags accessibility issues  
  *Escalation Highlight: Accessibility blocker found; escalates to PM and DEV for urgent fix.*

**Afternoon:**
- Prepares UI assets
- Reviews A/B test results
- Updates design documentation

**Edge Case:**
- User feedback reveals a critical usability flaw post-release; UX escalates to PM, triggers emergency design review.

---

## Collaboration & Escalation
- All agents participate in daily standup and sprint retrospectives
- Escalations follow the defined protocol in agent_roles_and_boundaries.md
- All communication is logged and monitored for continuous improvement
