# AGENTS.md

## Purpose

This document defines how AI agents (for example, Codex) must operate when working on the **Sales Report Processor (SRP)** project.

It consolidates:

- project goals
- MVP boundaries
- architecture decisions
- development workflow
- local AI operating rules
- project behavior expectations

The goal is to ensure **consistent, high-quality, scoped, and implementation-ready output**.

This file is a **local project behavior and scope guide**.

It is **not** the primary authority for:
- current ticket state
- next ticket sequence
- delivery readiness
- implementation truth when docs are stale

Those are governed by the SRP delivery authority model.

---

# 1. Project Overview

## System

Sales Report Processor (SRP) — MVP

## Goal

Transform unstructured supplier reports (TXT/PDF) into structured data and expose actionable insights.

## Core Pipeline

1. Upload report (TXT/PDF)
2. Validate file
3. Parse TXT report
4. Store structured data
5. Expose via API
6. Display in dashboard

## Business Context

- Used in B2B industrial sales workflows
- Reports are currently processed manually
- The system reduces:
  - manual effort
  - decision delays
  - lack of visibility

---

# 2. MVP Scope

## Included

- File upload API (`POST /api/reports/upload/`)
- TXT parsing engine
- Structured data storage
- Retrieval API (`GET /api/reports/`)
- Basic dashboard

## Not Included

- Authentication
- Advanced frontend (React)
- Complex PDF parsing
- Machine learning
- SalesApp integration
- Docker

## Scope Rule

If it is not required for MVP:
→ **DO NOT IMPLEMENT**

Use `project_instructions_SRP.md` as the final authority for MVP boundaries.

---

# 3. Tech Stack

- Backend: Django + Django REST Framework
- Database:
  - MVP: SQLite
  - Production: PostgreSQL
- Parsing: Python (`open`, `re`)
- Frontend: Django templates (minimal)
- Python: 3.12

---

# 4. Current System State Rule

This file does **not** hardcode the current ticket or current delivery focus.

Current delivery focus must be resolved dynamically using the SRP delivery-governance system.

Use:

1. explicit live Jira ticket if provided
2. otherwise `jira_backlog_SRP.md`
3. `AI_CONTEXT_SRP.md` for project-state orientation
4. codebase truth for implementation reality
5. `AI_DELIVERY_SYSTEM_SRP.md` for delivery control

### What is broadly true at project level

- Project setup exists
- Django scaffold exists
- File upload API exists
- File validation exists
- TXT parsing exists
- Parsed-data persistence work exists in the project
- Retrieval API work is complete under `SRP-12`
- Dashboard work is complete under `SRP-13`
- The next planned delivery stage is `SRP-14` for validation and error handling

Because implementation can move ahead of narrative docs, **codebase truth must override stale narrative state statements** when the two diverge. 

---

# 5. Project Structure

```text
sales-report-processor/
├── backend/
│   ├── srp/
│   ├── reports/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services/
│   │   └── tests/
│   └── media/
├── frontend/
├── docs/
│   ├── AI/
│   └── ...
└── requirements.txt
```

---

# 6. Development Workflow

## Branching

* Use feature branches:

  * `feature/SRP-XXX-description`

## Commits

* Small and meaningful
* One logical change per commit

## Execution Strategy

* Build in small steps
* Each step must work
* Each feature must be testable
* One ticket at a time
* No hidden scope expansion

## Engineering Standards

All SRP work must respect these software lifecycle principles:

* software design before implementation when the feature introduces new structure or flow
* separation of concerns between view, service, persistence, parsing, and presentation layers
* high cohesion inside each file/module
* loose coupling between layers and responsibilities
* security-first defaults and explicit validation
* tests for behavior-changing work
* documentation updates as part of implementation closure, not as optional cleanup

---

# 7. Delivery Governance Rule

This file provides local project behavior and scope discipline.

For **ticket sequencing, current focus resolution, readiness before implementation, authority levels, and ticket lifecycle**, the agent must use:

* `AI_DELIVERY_SYSTEM_SRP.md`
* explicit live Jira ticket if provided
* otherwise `jira_backlog_SRP.md`
* `AI_CONTEXT_SRP.md`
* codebase truth

This file must **not** be treated as the primary authority for current ticket state if it becomes stale. 

---

# 8. Local Authority Order

When conflicts arise inside SRP, follow this practical order:

1. `project_instructions_SRP.md`

   * MVP scope
   * out-of-scope boundaries
   * completion definition

2. Explicit live Jira ticket if provided; otherwise `jira_backlog_SRP.md`

   * current ticket
   * next valid ticket
   * story/subtask hierarchy
   * delivery sequence

3. `AI_CONTEXT_SRP.md`

   * project-state orientation
   * current interpreted status snapshot

4. Codebase truth

   * what is actually implemented
   * what is wired
   * what is tested
   * what is runnable

5. Local `AGENTS.md` + SRP AI docs

   * project behavior
   * implementation discipline
   * output style
   * local workflow rules

If the conflict is about **what is implemented**, codebase truth wins.
If the conflict is about **what should be worked now**, live Jira or backlog sequence wins. 

---

# 9. AI Operating System (MANDATORY)

## Core Principles

1. Be practical and direct
2. Prefer implementation over theory
3. Avoid unnecessary complexity
4. Never assume missing features
5. Always choose the simplest working solution

## Hard Rules

* No features outside the current ticket scope
* No over-engineering
* No invented architecture
* Always produce runnable code
* Always align with existing structure
* Never let stale docs override implementation truth
* Never infer ticket readiness without using the delivery-governance layer

---

# 10. AI Runtime Loop (MANDATORY)

Every response must follow:

### 1. Interpret

Understand:

* request type
* whether it is diagnosis, planning, implementation, review, or closure work

### 2. Scope & Validate

Check:

* Is it inside the current ticket?
* Is it MVP-compliant?
* Is it aligned with project structure?
* Is the ticket actually ready under `AI_DELIVERY_SYSTEM_SRP.md`?

If not:
→ stop and state the reason explicitly

### 3. Plan

Define:

* files to change
* smallest valid steps
* tests needed
* docs/context updates needed

### 4. Output

Use the correct local output contract.

### 5. Check

Confirm:

* simple
* runnable
* scoped
* aligned with current authority level

---

# 11. Output Contracts

## Rule

Use the **smallest possible format** that fits the task.

Use `AI_OUTPUT_CONTRACTS_SRP.md` for output shape. 

### Backend Implementation

Must include:

* Objective
* Scope (ticket + files)
* Code
* Validation steps
* Success criteria
* Failure cases

### Jira Story

Must include:

* Description
* Scope
* Acceptance criteria
* Dependencies

### Jira Subtask

Must include:

* Purpose
* Scope
* Deliverables
* Technical notes

### Review

Must include:

* Findings
* Risks
* Recommendation

---

# 12. Key Technical Decisions

## Backend

* Always Django / DRF

## Database

* SQLite for MVP
* No SQLite-specific logic

## File Parsing

* TXT → Python (`open`, `re`)
* PDF → accepted only, not parsed in MVP

## Storage

* Uploaded files → `FileField`
* Parsed data → relational models

## API Design

* `POST /api/reports/upload/`
* `GET /api/reports/`
* `GET /api/reports/{id}/`

No authentication in MVP.

---

# 13. Data Model Architecture (Target)

Hierarchy:

```text
ParsedReport
└── CustomerSection
    └── ParsedItem
        └── ContinuationRow
```

Plus:

* customer totals
* report totals

---

# 14. Parsing System Reality

Parser already delivers:

* metadata
* customer blocks
* main rows
* continuation rows
* totals

Parsing output is suitable for persistence.

---

# 15. Quality Rules

* Validate all inputs
* Clear error messages
* Keep code readable
* Avoid premature optimization
* Tests are required whenever behavior changes in a meaningful way
* Lightweight is fine, but unverified critical behavior is not

---

# 16. Uncertainty Rule

If something is unclear:

* state the assumption explicitly
* choose the safest minimal solution
* do **not** invent missing structure
* do **not** silently skip delivery-state conflicts
* do **not** guess the current ticket without using the delivery-governance authority chain

---

# 17. Definition of Done (MVP)

System is complete when:

1. File upload works
2. Files are validated
3. Files are stored
4. TXT is parsed
5. Data is stored in DB
6. API returns processed data
7. Dashboard shows data
8. Errors are handled correctly

Use `project_instructions_SRP.md` as the final authority for MVP completion. 

---

# 18. Agent Behavior Summary (CRITICAL)

When working on this project, the agent must:

* work **ticket by ticket**
* stay **strictly within scope**
* prefer **simple over perfect**
* produce **working code, not vague ideas**
* follow **existing structure exactly**
* never “improve” beyond MVP
* resolve **current focus automatically** through the delivery-governance layer
* state:

  * current focus
  * focus source
  * authority level
  * ticket readiness
    at the start of every substantial SRP delivery session

---

# 19. Recommended Usage (for Humans)

When starting a new SRP task:

1. load the SRP local AI system
2. reference `AI_DELIVERY_SYSTEM_SRP.md`
3. set the authority level for the session
4. provide the current Jira ticket if available
5. ask for:

   * diagnosis
   * plan
   * implementation
   * review
   * closure support

Example:

```text
Load the SRP local AI system and follow AI_DELIVERY_SYSTEM_SRP.md.

Agent authority for this session: Level 2 — Plan Only.

Current Jira ticket: SRP-13

Task: automatically resolve current focus, confirm readiness, and produce the minimal implementation plan.
```
