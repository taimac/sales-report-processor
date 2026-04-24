# AI Operating System – SRP

## Purpose

Guide AI behavior for building the SRP MVP.
This file is the single authority on principles.
All other files define mechanics only.

---

## Core Principles

1. Be practical and direct
2. Focus on implementation over theory
3. Avoid unnecessary complexity
4. Do not assume features exist
5. If unsure → do not assume → keep solution minimal
6. Design before building when the feature introduces new structure or flow
7. Prefer separation of concerns, high cohesion, and loose coupling
8. Treat security and tests as default engineering responsibilities
9. Treat documentation as part of the software lifecycle, not post-work cleanup

---

## Authority Order

When there is a conflict, resolve in this order:

1. `project_instructions_SRP.md`
2. Current Jira ticket (from `jira_backlog_SRP.md`)
3. `AI_CONTEXT_SRP.md` (actual state of the project)
4. Codebase reality

---

## Hard Rules

- No features outside the current ticket scope
- No over-engineering
- Prefer the simplest working solution
- Always produce runnable, copy-paste ready code
- Never invent project structure — use `AI_CONTEXT_SRP.md`
- Keep business logic out of templates whenever possible
- Do not collapse service, view, and persistence responsibilities into one layer
- Add or update tests when behavior changes
- Update delivery-state docs when implementation changes affect project truth

---

## Output Style

- Structured using `AI_OUTPUT_CONTRACTS_SRP.md`
- Clear and direct
- Minimal explanation — code speaks for itself
