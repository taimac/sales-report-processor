# AI Bootstrap Prompt – SRP

## Purpose

Initialize the SRP AI system for a new conversation.

Copy this prompt as the first message when starting a new SRP session.

This bootstrap must ensure the SRP agent loads not only implementation rules, but also the **delivery-governance layer** that controls:
- current ticket selection
- readiness before implementation
- authority level for the session
- delivery flow from diagnosis to closure
- mandatory engineering principles that govern design, cohesion, coupling, security, tests, and documentation continuity

---

## Bootstrap Prompt

You are working on the **Sales Report Processor (SRP)** — a Django/DRF MVP
that accepts TXT and PDF supplier reports, extracts structured data from
TXT reports, stores it in SQLite (migrating to PostgreSQL in production),
exposes it via a REST API, and displays it on a basic dashboard.

The repo is at: `sales-report-processor/`  
Django project lives inside: `backend/`  
Python version: `3.12`  
Venv is at root level.

Load and follow these files in order:

1. `AI_OS_SRP.md`  
   → principles, authority order, project-level operating rules

2. `AI_DELIVERY_SYSTEM_SRP.md`  
   → delivery governance, authority ladder, readiness gate, ticket lifecycle

3. `AI_CONTEXT_SRP.md`  
   → current project state, backlog status, target structure

4. `AI_RUNTIME_LOOP_SRP.md`  
   → reasoning and response flow

5. `AI_DECISION_RULES_SRP.md`  
   → concrete implementation decisions

6. `AI_OUTPUT_CONTRACTS_SRP.md`  
   → output formats

7. `project_instructions_SRP.md`  
   → MVP scope, completion definition, out-of-scope boundaries

8. local `AGENTS.md`  
   → project behavior, workflow expectations, technical constraints

---

## Default Startup Rule

Do **not** start coding immediately by default.

At the start of every SRP session, first determine:

1. **Current authority level**
   - Level 1 → Diagnose Only
   - Level 2 → Plan Only
   - Level 3 → Implement Locally
   - Level 4 → Delivery Package
   - Level 5 → Full Ticket Cycle

2. **Current ticket**
   - explicit live Jira ticket if provided
   - otherwise derive from `jira_backlog_SRP.md` or current SRP context

3. **Ticket readiness**
   - check the Ticket Readiness Gate from `AI_DELIVERY_SYSTEM_SRP.md`

Only implement if the current authority level allows it **and** the Ticket Readiness Gate is fully satisfied.

When implementation is allowed, apply SRP engineering standards by default:

- design before build for non-trivial features
- separation of concerns
- high cohesion
- loose coupling
- security-first defaults
- tests for behavior changes
- documentation updates as part of delivery

---

## Default Mode

Default to:

- **Diagnosis** if no ticket is provided
- **Planning** if ticket exists but readiness is incomplete
- **Implementation** only if:
  - ticket is explicit
  - ticket is in sequence
  - MVP scope is confirmed
  - acceptance criteria are clear enough
  - codebase gap is confirmed
  - files/tests are clear

Do not assume implementation is the correct default.

---

## Session Start Template

Use this at the beginning of an SRP session:

```text
Load and follow the SRP local AI system.

Authority level for this session: Level [1/2/3/4/5].

Current Jira ticket: [SRP-XXX or “not provided”]

Task: [brief description]

Before acting, determine:
1. current ticket
2. whether it is the correct next ticket
3. whether the Ticket Readiness Gate is satisfied
4. whether the current authority level allows diagnosis, planning, or implementation

If readiness is incomplete:
- stop at diagnosis or plan
- state the missing item explicitly

If documentation and codebase disagree:
- use delivery authority order from AI_DELIVERY_SYSTEM_SRP.md
- prefer codebase truth for implementation state
- do not silently assume ticket state
