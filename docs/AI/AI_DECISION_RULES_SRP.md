# AI Decision Rules – SRP

## Purpose

Concrete decision tables for implementation choices.
Principles live in `AI_OS_SRP.md`. This file is mechanics only.

---

## Backend Framework

Always Django / DRF. No exceptions for MVP.

---

## Architecture Rules

| Need | Decision |
|------|----------|
| Business logic | Prefer a dedicated service layer before inflating views |
| Views | Handle request/response orchestration, not decision-heavy domain logic |
| Templates | Render prepared context only; avoid embedded operational rules |
| Module design | Prefer high cohesion and small responsibilities |
| Coupling | Prefer explicit interfaces between layers and avoid unnecessary cross-layer dependencies |
| Security | Validate input and choose safe defaults before convenience shortcuts |
| Tests | Add focused tests near the changed behavior before considering the work complete |

---

## Database

| Phase | Database | Reason |
|-------|----------|--------|
| MVP (now) | SQLite | Zero config, built into Django, sufficient for MVP |
| Production | PostgreSQL | Swap `DATABASES` in settings + run migrate |

No SQLite-specific features — keep all queries standard Django ORM
to ensure zero friction when migrating to PostgreSQL.

---

## File Parsing

| File type | Tool | Notes |
|-----------|------|-------|
| TXT | Python built-in (`open`, `re`) | Line iteration + key:value regex |
| PDF | `pdfplumber` | Future phase — accepted on upload, not parsed yet |

---

## Data Storage

| Situation | Decision |
|-----------|----------|
| Uploaded file | `FileField` on `UploadedReport` model |
| Parsed TXT fields | Separate `ParsedReport` model with `JSONField` |
| SQLite DB file | `backend/db.sqlite3` — never commit to repo |

---

## API Design

| Need | Decision |
|------|----------|
| File upload | `POST /api/reports/upload/` — `multipart/form-data` |
| List reports | `GET /api/reports/` |
| Get one report | `GET /api/reports/{id}/` |
| No auth for MVP | Skip authentication — not in MVP scope |

---

## Frontend (MVP)

| Need | Decision |
|------|----------|
| Dashboard | Simple Django template or minimal HTML view |
| No React for MVP | React SPA is a future phase |
| Data display | Summary stats + actionable tables/worklists prepared by the backend |
| Template responsibility | Presentation only; no decision-heavy operational logic in templates |

---

## File Locations

| What | Where |
|------|-------|
| Django project | `backend/` |
| Uploaded files | `backend/media/reports/` |
| SQLite database | `backend/db.sqlite3` |
| All Django commands | Run from `backend/` |
| Venv activation | Run from repo root: `source venv/bin/activate` |

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

---

## Documentation Rule

When implementation changes project meaning, also update the relevant docs:

- `README.md` for public/local project usage
- `AI_CONTEXT_SRP.md` for current interpreted project state
- backlog-derived delivery docs when ticket state changes

Documentation is part of the implementation lifecycle for SRP.
