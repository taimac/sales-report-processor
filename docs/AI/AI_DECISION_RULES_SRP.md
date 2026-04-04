# AI Decision Rules – SRP

## Purpose

Concrete decision tables for implementation choices.
Principles live in `AI_OS_SRP.md`. This file is mechanics only.

---

## Backend Framework

Always Django + DRF. No exceptions for MVP.

---

## File Parsing

| File type | Tool | Notes |
|-----------|------|-------|
| TXT | Python built-in (`open`, `str`, `re`) | Start with line iteration; add regex only if needed |
| PDF | `pdfplumber` | Primary choice — handles text and tables cleanly |
| PDF fallback | `PyPDF2` | Only if `pdfplumber` fails for a specific file |

---

## Data Storage

| Situation | Decision |
|-----------|----------|
| Structured extracted data | Django model → PostgreSQL |
| Raw uploaded file | `FileField` on the Report model |
| File already parsed | Store result in related `ReportData` model |

---

## API Design

| Need | Decision |
|------|----------|
| File upload | `POST /api/reports/` with `multipart/form-data` |
| List reports | `GET /api/reports/` |
| Get one report + data | `GET /api/reports/{id}/` |
| No auth for MVP | Skip authentication — not in MVP scope |

---

## Scope Gate

If a feature is not in the current Jira ticket:
→ do not implement it
→ note it as a future consideration if relevant

---

## Uncertainty Rule

If information is missing:
→ state the assumption explicitly
→ make the safest minimal choice
→ never invent file structure or completed features