# AI Bootstrap Prompt – SRP

## Purpose

Initialize the SRP AI system for a new conversation.
Copy this prompt as the first message when starting a new session.

---

## Bootstrap Prompt (copy-paste ready)

```
You are working on the Sales Report Processor (SRP) — a Django/DRF MVP
that accepts TXT and PDF supplier reports, extracts structured data,
stores it in PostgreSQL, and exposes it via a REST API.

Nothing exists yet. SRP-1 is the first task.

Load and follow these files in order:
1. AI_OS_SRP.md          ← principles and authority order
2. AI_CONTEXT_SRP.md     ← current project state and target structure
3. AI_RUNTIME_LOOP_SRP.md ← how to reason and respond
4. AI_DECISION_RULES_SRP.md ← concrete implementation decisions
5. AI_OUTPUT_CONTRACTS_SRP.md ← output formats

Mode: Implementation (default)

Current task: [PASTE JIRA TICKET HERE]
```

---

## Rules

- Always paste the current Jira ticket when starting implementation
- Do not start without a ticket — the scope gate depends on it
- Stay within MVP scope
- Prefer simple working solutions
- Produce code with clear steps