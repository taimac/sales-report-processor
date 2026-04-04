# Project Instructions – Sales Report Processor (SRP)

## Purpose

This project is a focused MVP to process supplier reports (TXT/PDF)
and convert them into structured data for sales and operational use.

It is part of the broader SalesApp vision, but developed independently.

---

## Development Approach

- Build in small, testable steps
- Focus on working features over completeness
- Avoid over-engineering
- Each feature must be demonstrable

---

## Workflow

- Use feature branches:
  feature/SRP-XXX-description

- Keep commits small and meaningful

- No need for full CI/CD at this stage

---

## Tech Stack

- Backend: Django / DRF
- Database: PostgreSQL
- Frontend: minimal (later stage)

---

## Quality Rules

- Validate inputs
- Handle errors clearly
- Keep code readable and simple

Tests are encouraged but lightweight for MVP.

---

## Goal

Deliver a working system that:

- accepts TXT/PDF reports
- extracts structured data
- exposes data via API

---

## Scope Rule

If a feature is not required for the MVP:
→ do not implement it