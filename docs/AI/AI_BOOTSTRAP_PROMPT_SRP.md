# AI Bootstrap Prompt – SRP

## Purpose

Initialize the SRP AI system for a new conversation.
Copy this prompt as the first message when starting a new session.

---

## Bootstrap Prompt (copy-paste ready)

```
You are working on the Sales Report Processor (SRP) — a Django/DRF MVP
that accepts TXT and PDF supplier reports, extracts structured data from
TXT reports, stores it in SQLite (migrating to PostgreSQL in production),
exposes it via a REST API, and displays it on a basic dashboard.

The repo is at: sales-report-processor/
Django project lives inside: backend/
Python version: 3.12
Venv is at root level.

Current state: SRP-1 is Done. Django project does not exist yet.

Load and follow these files in order:
1. AI_OS_SRP.md              ← principles and authority order
2. AI_CONTEXT_SRP.md         ← current project state and target structure
3. AI_RUNTIME_LOOP_SRP.md    ← how to reason and respond
4. AI_DECISION_RULES_SRP.md  ← concrete implementation decisions
5. AI_OUTPUT_CONTRACTS_SRP.md ← output formats

Mode: Implementation (default)

Current task: SRP-9 – Django Project and App Scaffold
```

---

## Rules

- Always paste the current Jira ticket when starting implementation
- Do not start without a ticket — the scope gate depends on it
- Stay within MVP scope
- Prefer simple working solutions
- Produce code with clear steps