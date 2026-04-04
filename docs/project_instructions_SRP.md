# Project Instructions – Sales Report Processor (SRP)

## Purpose

Build a backend-driven MVP that transforms unstructured supplier reports (TXT/PDF)
into structured data and presents actionable insights through a simple dashboard.

Part of the broader SalesApp vision, developed independently.

---

## Development Approach

- Build in small, testable steps
- Focus on working features over completeness
- Avoid over-engineering
- Each feature must be demonstrable

---

## Workflow

- Use feature branches: `feature/SRP-XXX-description`
- Keep commits small and meaningful
- No CI/CD required at MVP stage

---

## Tech Stack

- Backend: Django / DRF
- Database: SQLite (MVP) → PostgreSQL (production)
- Parsing: Python (regex / text processing)
- Frontend (MVP): simple server-rendered view or minimal interface
- File types: TXT and PDF upload, TXT parsing (initial)
- Environment: local (Docker planned)

---

## Quality Rules

- Validate all inputs
- Handle errors with clear messages
- Keep code readable and simple
- Tests are encouraged but lightweight for MVP

---

## MVP Complete Definition

The MVP is complete when ALL of the following are true:

1. TXT and PDF files can be uploaded via `POST /api/reports/upload/`
2. Files are validated (type and presence)
3. Uploaded files are stored to disk
4. TXT reports are parsed and key fields extracted:
   - order number, client, product, quantity, status
5. Extracted data is stored in structured format in the database
6. `GET /api/reports/` returns processed report data
7. A basic dashboard displays summary and table of extracted records
8. Invalid files are rejected with clear error messages

---

## Scope Rule

If a feature is not required for the MVP definition above:
→ do not implement it
→ note it as a future item if relevant

---

## Out of Scope (Future Phases)

- Advanced PDF parsing (complex layouts)
- Authentication / user management
- Browser automation
- Advanced frontend (React SPA)
- Machine learning / predictive analytics
- Full SalesApp integration
- Docker setup