# AI Context – SRP

## Project

Sales Report Processor (SRP) – MVP

---

## Goal

Accept TXT and PDF supplier reports, parse key fields from TXT reports,
store structured data, expose it via API, and display it on a basic dashboard.

---

## Current State

- SRP-1 (Initial Project Setup) is **Done**
- Repo exists at `sales-report-processor/`
- Virtual environment configured (`venv/`, Python 3.12)
- `requirements.txt` exists at root
- `backend/` directory exists but is empty — Django project not created yet
- `frontend/` directory exists but is empty — basic dashboard planned for MVP
- No Django project, no apps, no models, no endpoints
- SRP-9 (Django Project and App Scaffold) is the next task

---

## Stack

- Backend: Django / DRF
- Database: SQLite (MVP) → PostgreSQL (production)
- Parsing: Python (regex / text processing)
- Frontend (MVP): simple server-rendered view or minimal interface
- File types: TXT and PDF upload — TXT parsing initial phase
- Python: 3.12

---

## Actual Repo Structure (current)

```
sales-report-processor/
├── backend/                  ← Django project goes here (SRP-9)
├── docs/
│   ├── AI/
│   │   ├── AI_BOOTSTRAP_PROMPT_SRP.md
│   │   ├── AI_CONTEXT_SRP.md
│   │   ├── AI_DECISION_RULES_SRP.md
│   │   ├── AI_OS_SRP.md
│   │   ├── AI_OUTPUT_CONTRACTS_SRP.md
│   │   └── AI_RUNTIME_LOOP_SRP.md
│   ├── jira_backlog_SRP.md
│   └── project_instructions_SRP.md
├── fetch_jira_backlog_srp.py
├── frontend/                 ← basic dashboard planned for MVP
├── LICENSE
├── README.md
├── requirements.txt
└── venv/
```

---

## Target Repo Structure (once SRP-9 is done)

```
sales-report-processor/
├── backend/
│   ├── manage.py
│   ├── srp/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── reports/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   └── media/                ← uploaded files saved here
├── frontend/                 ← basic dashboard (later in MVP)
├── docs/
│   ├── AI/
│   └── ...
├── .env.example
├── requirements.txt
└── venv/
```

---

## Important Notes

- All Django commands run from `backend/`
- `venv` is at root level — activate from root: `source venv/bin/activate`
- `requirements.txt` is at root level
- `fetch_jira_backlog_srp.py` is a utility script at root — do not modify
- SQLite database file will be at `backend/db.sqlite3` — do not commit it

---

## MVP Definition

MVP is complete when:

1. TXT and PDF files can be uploaded via `POST /api/reports/upload/`
2. Files are validated (type and presence)
3. Uploaded files are stored to `backend/media/reports/`
4. TXT reports are parsed and key fields extracted:
   - order number, client, product, quantity, status
5. Extracted data is stored in structured format in SQLite
6. `GET /api/reports/` returns processed report data
7. A basic dashboard displays summary and table of extracted records
8. Invalid files are rejected with clear error messages

---

## Jira Structure

```
[Epic]  SRP-2 – Sales Report Processor MVP
  ├─ SRP-1    Initial Project Setup             ✅ Done
  ├─ SRP-9    Django Project and App Scaffold   ✅ Done  
  ├─ SRP-3    File Upload API                   ⬜ In Progress
  │    ├─ SRP-4   Create UploadedReport model   ✅ Done  
  │    ├─ SRP-5   Implement upload API endpoint ✅ Done 
  │    ├─ SRP-6   Add file validation (TXT and PDF)     ⬜ To Do  ← next
  │    ├─ SRP-7   Add backend tests for upload endpoint ⬜ To Do
  │    └─ SRP-8   Document upload endpoint behavior     ⬜ To Do
  ├─ SRP-10   TXT Parsing Engine                ⬜ To Do
  ├─ SRP-11   Parsed Data Models                ⬜ To Do
  ├─ SRP-12   Processed Data Retrieval API      ⬜ To Do
  ├─ SRP-13   Basic Dashboard View              ⬜ To Do
  ├─ SRP-14   Error Handling and Validation     ⬜ To Do
  └─ SRP-15   Documentation and Demo Readiness  ⬜ To Do
```

---

## Backlog Order

1. ~~SRP-1 – Initial Project Setup~~ ✅ Done
2. SRP-9  – Django Project and App Scaffold
3. SRP-3  – File Upload API (SRP-4 → 5 → 6 → 7 → 8)
4. SRP-10 – TXT Parsing Engine
5. SRP-11 – Parsed Data Models
6. SRP-12 – Processed Data Retrieval API
7. SRP-13 – Basic Dashboard View
8. SRP-14 – Error Handling and Validation
9. SRP-15 – Documentation and Demo Readiness
