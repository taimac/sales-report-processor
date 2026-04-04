# AI Runtime Loop – SRP

## Purpose

Define the reasoning process for SRP work.

The goal is to keep outputs:
- practical
- scoped
- implementation-ready

---

## Core Principle

Every response must follow:

Interpret → Scope → Validate → Plan → Output → Check

---

## Step 1 – Interpret

Understand:
- what is being asked
- whether it is documentation, Jira, architecture, or implementation
- what the smallest useful output is

---

## Step 2 – Scope

Check against:
1. `project_instructions_SRP.md`
2. current Jira ticket or current task
3. current codebase reality

Rule:
- if it is outside MVP scope, do not expand into it

---

## Step 3 – Validate

Before proposing anything, verify:
- does it fit the MVP?
- is it consistent with the current repo structure?
- is it simple enough for this stage?
- does it avoid over-engineering?

---

## Step 4 – Plan

Define:
- files affected
- components involved
- minimal sequence of implementation
- required validation or tests

Keep the plan small and executable.

---

## Step 5 – Output

Produce:
- clear
- structured
- copy-paste ready output

Use `AI_OUTPUT_CONTRACTS_SRP.md`.

---

## Step 6 – Check

Before finalizing, verify:
- scope is respected
- no unnecessary complexity was added
- steps are implementable
- wording is direct and practical

---

## Uncertainty Rule

If information is missing:
- state uncertainty explicitly
- make the safest minimal assumption
- do not invent project structure or completed features