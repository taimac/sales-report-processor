# AI Context – SRP

## Project

Sales Report Processor (SRP) – MVP

---

## Goal

Accept TXT and PDF supplier reports, validate and store them,
and return a structured response via DRF API.

---

## Current State

- SRP-1 (Initial Project Setup) is **Done**
- Repo exists at `sales-report-processor/`
- Virtual environment configured (`venv/`, Python 3.12)
- `requirements.txt` exists at root
- `backend/` directory exists but is empty — Django project not created yet
- `frontend/` directory exists but is empty — out of scope for MVP
- No Django project, no apps, no models, no endpoints
- SRP-9 (Django Project and App Scaffold) is the next task

---

## Stack

- Backend: Django / DRF
- Database: PostgreSQL
- File types: TXT and PDF
- Frontend: not in scope
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
├── frontend/                 ← out of scope for MVP
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
│   └── reports/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── tests/
├── docs/
│   ├── AI/
│   └── ...
├── .env              ← local only, not committed
├── .env.example      ← committed
├── requirements.txt
└── venv/
```

---

## Important Notes

- All Django commands run from `backend/`
- `venv` is at root level — activate from root: `source venv/bin/activate`
- `requirements.txt` is at root level
- `fetch_jira_backlog_srp.py` is a utility script at root — do not modify

---

## MVP Definition

MVP is complete when:

1. A TXT or PDF file can be uploaded via `POST /api/reports/upload/`
2. The file is validated (type = txt or pdf, not empty)
3. The file is saved to `backend/media/reports/`
4. An `UploadedReport` record is created in PostgreSQL
5. The response returns the report ID, filename, and status
6. Invalid files are rejected with a clear error message

---

## Jira Structure

```
[Epic]  SRP-2 – Sales Report Processor MVP
  ├─ SRP-1   Initial Project Setup              ✅ Done
  ├─ SRP-9   Django Project and App Scaffold    ⬜ To Do  ← next
  └─ SRP-3   File Upload API                    ⬜ To Do
       ├─ SRP-4   Create UploadedReport model
       ├─ SRP-5   Implement upload API endpoint
       ├─ SRP-6   Add file validation (TXT and PDF)
       ├─ SRP-7   Add backend tests for upload endpoint
       └─ SRP-8   Document upload endpoint behavior
```

---

## Backlog Order

1. ~~SRP-1 – Initial Project Setup~~ ✅ Done
2. SRP-9 – Django Project and App Scaffold
3. SRP-3 – File Upload API
   - SRP-4 → SRP-5 → SRP-6 → SRP-7 → SRP-8