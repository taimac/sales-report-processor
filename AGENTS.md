# AGENTS.md

## Purpose

This document defines how AI agents (e.g., Codex) must operate when working on the **Sales Report Processor (SRP)** project.

It consolidates:

* Project goals
* Architecture decisions
* Development workflow
* AI operating rules
* Current system state

The goal is to ensure **consistent, high-quality, scoped, and implementation-ready output**.

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

* Used in B2B industrial sales workflows
* Reports are currently processed manually
* System reduces:

  * manual effort
  * decision delays
  * lack of visibility

---

# 2. MVP Scope

## Included

* File upload API (`POST /api/reports/upload/`)
* TXT parsing engine
* Structured data storage
* Retrieval API (`GET /api/reports/`)
* Basic dashboard

## Not Included

* Authentication
* Advanced frontend (React)
* Complex PDF parsing
* Machine learning
* SalesApp integration
* Docker

## Scope Rule

If it is not required for MVP → **DO NOT IMPLEMENT**

---

# 3. Tech Stack

* Backend: Django + Django REST Framework
* Database:

  * MVP: SQLite
  * Production: PostgreSQL
* Parsing: Python (`open`, `re`)
* Frontend: Django templates (minimal)
* Python: 3.12

---

# 4. Current System State

## Completed

* Project setup
* Django scaffold
* File upload API
* File validation
* TXT parsing engine (FULLY DONE)

## Current Focus

SRP-11 — Parsed Data Models

## Next Steps

* Persist parsed data
* Build retrieval API
* Build dashboard

---

# 5. Project Structure

```
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

---

# 7. AI Operating System (MANDATORY)

## Core Principles

1. Be practical and direct
2. Prefer implementation over theory
3. Avoid unnecessary complexity
4. Never assume missing features
5. Always choose the simplest working solution

---

## Authority Order (STRICT)

When conflicts arise, follow:

1. `project_instructions_SRP.md`
2. Current Jira ticket
3. `AI_CONTEXT_SRP.md`
4. Codebase

---

## Hard Rules

* No features outside ticket scope
* No over-engineering
* No invented architecture
* Always produce runnable code
* Always align with existing structure

---

# 8. AI Runtime Loop (MANDATORY)

Every response MUST follow:

### 1. Interpret

Understand:

* request type (implementation, planning, etc.)

### 2. Scope & Validate

* Is it inside the Jira ticket?
* Is it MVP-compliant?
* Is it aligned with project structure?

If NOT → STOP

### 3. Plan

* Files to change
* Minimal steps

### 4. Output

* Use correct output contract

### 5. Check

* Is it simple?
* Is it runnable?
* Is it scoped?

---

# 9. Output Contracts

## Rule

Use the **smallest possible format**.

---

## Backend Implementation

Must include:

* Objective
* Scope (ticket + files)
* Code (copy-paste ready)
* Validation steps
* Success criteria
* Failure cases

---

## Jira Story

Must include:

* Description
* Scope (included / not included)
* Acceptance criteria
* Dependencies

---

## Jira Subtask

Must include:

* Purpose
* Scope
* Deliverables
* Technical notes

---

## Review

Must include:

* Findings
* Risks
* Recommendation

---

# 10. Key Technical Decisions

## Backend

* Always Django / DRF

## Database

* SQLite (MVP)
* No SQLite-specific logic

## File Parsing

* TXT → Python (`open`, `re`)
* PDF → accepted only (no parsing yet)

## Storage

* Uploaded files → `FileField`
* Parsed data → relational models

---

## API Design

* `POST /api/reports/upload/`
* `GET /api/reports/`
* `GET /api/reports/{id}/`

No authentication (MVP)

---

# 11. Data Model Architecture (Target)

Hierarchy:

```
ParsedReport
└── CustomerSection
    └── ParsedItem
        └── ContinuationRow
```

Plus:

* Customer totals
* Report totals

---

# 12. Parsing System Reality

Parser already delivers:

* metadata
* customer blocks
* main rows
* continuation rows
* totals

Output is **ready for persistence (SRP-11)**

---

# 13. Quality Rules

* Validate all inputs
* Clear error messages
* Keep code readable
* Avoid premature optimization
* Tests: encouraged, lightweight

---

# 14. Uncertainty Rule

If something is unclear:

* State assumption explicitly
* Choose safest minimal solution
* DO NOT invent missing structure

---

# 15. Definition of Done (MVP)

System is complete when:

1. File upload works
2. Files are validated
3. Files are stored
4. TXT is parsed
5. Data is stored in DB
6. API returns processed data
7. Dashboard shows data
8. Errors handled correctly

---

# 16. Agent Behavior Summary (CRITICAL)

When working on this project, the agent MUST:

* Work **ticket by ticket**
* Stay **strictly within scope**
* Prefer **simple over perfect**
* Produce **working code, not ideas**
* Follow **existing structure exactly**
* Never “improve” beyond MVP

---

# 17. Recommended Usage (for Humans)

When starting a new task:

1. Paste the current Jira ticket
2. Reference this file
3. Ask for:

   * Subtasks OR
   * Implementation

---

This `AGENTS.md` now acts as your **single source of truth for AI-assisted development**.

---
