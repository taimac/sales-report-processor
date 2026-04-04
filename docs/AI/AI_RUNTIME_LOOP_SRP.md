# AI Runtime Loop – SRP

## Purpose

Define the reasoning process for every SRP response.

Goal: keep outputs practical, scoped, and implementation-ready.

---

## Core Principle

Every response must follow this loop:

**Interpret → Scope & Validate → Plan → Output → Check**

---

## Step 1 – Interpret

Understand:
- What is being asked
- Whether it is documentation, Jira, architecture, or implementation
- What the smallest useful output is

---

## Step 2 – Scope & Validate

Check against, in order:
1. `project_instructions_SRP.md`
2. Current Jira ticket
3. `AI_CONTEXT_SRP.md` (actual project state)

Ask:
- Is this inside the current ticket's scope?
- Is it consistent with the target repo structure?
- Is it simple enough for this stage?
- Does it avoid over-engineering?

If outside scope → stop and state it explicitly.
If uncertain about state → check `AI_CONTEXT_SRP.md` before assuming.

---

## Step 3 – Plan

Define:
- Files to create or modify
- Components involved (model, serializer, view, parser, etc.)
- Minimal sequence of steps
- Any validation or tests needed

Keep the plan small and executable.
One ticket = one plan = one output.

---

## Step 4 – Output

Produce output using `AI_OUTPUT_CONTRACTS_SRP.md`.

Choose the smallest contract that fits:
- Implementation task → Contract 4
- Jira story → Contract 2
- Subtask → Contract 3
- Analysis or review → Contract 1

---

## Step 5 – Check

Before finalizing, verify:
- Scope respected — nothing beyond the ticket
- No unnecessary complexity added
- Steps are implementable as written
- Wording is direct and practical
- Code is runnable without modification

---

## Uncertainty Rule

If information is missing:
- State the assumption explicitly at the top of the response
- Make the safest minimal assumption
- Never invent project structure or completed features
