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
- SRP-9 (Django Project and App Scaffold) is **Done**
- SRP-3 (File Upload API) is **Done** (including SRP-4 → SRP-8)

### Implemented So Far

- Django project initialized inside `backend/`
- `reports` app created and registered
- SQLite configured for MVP
- Upload model (`UploadedReport`) implemented
- File upload endpoint available at:
  - `POST /api/reports/upload/`
- File validation implemented:
  - Accepts `.txt` and `.pdf`
  - Rejects invalid or missing files with clear errors
- Files stored under:
  - `backend/media/reports/`
- Backend tests implemented and passing
- Upload endpoint documented in README

---

## Stack

- Backend: Django / DRF
- Database: SQLite (MVP) → PostgreSQL (production)
- Parsing: Python (regex / text processing)
- Frontend (MVP): simple server-rendered view or minimal interface
- File types: TXT and PDF upload — TXT parsing initial phase
- Python: 3.12

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
  ├─ SRP-1    Initial Project Setup               ✅ Done
  ├─ SRP-9    Django Project and App Scaffold     ✅ Done
  ├─ SRP-3    File Upload API                     ✅ Done
  │    ├─ SRP-4    Create upload data model            ✅ Done
  │    ├─ SRP-5    Implement upload API endpoint       ✅ Done
  │    ├─ SRP-6    Add file validation for TXT/PDF uploads ✅ Done
  │    ├─ SRP-7    Add backend tests for upload endpoint ✅ Done
  │    └─ SRP-8    Document upload endpoint behavior   ✅ Done
  ├─ SRP-10   TXT Parsing Engine                  ✅ Done
  │    ├─ SRP-16   TXT Reader and Header Metadata Extraction ✅ Done
  │    ├─ SRP-17   Line Classification and Report Structure Detection ✅ Done
  │    ├─ SRP-18   Parse Production, Delivery, and Quantity Columns ✅ Done
  │    ├─ SRP-19   Parse Commercial, Credit, and Reference Columns ✅ Done
  │    ├─ SRP-20   Continuation Row Parsing and Parent Item Attachment ✅ Done
  │    ├─ SRP-21   Client and Grand Total Extraction   ✅ Done
  │    ├─ SRP-22   Final Parser Assembly and Real Sample Tests ✅ Done
  │    └─ SRP-23   Parse Core Main Row Identity and Product Columns ✅ Done
  ├─ SRP-11   Parsed Data Models                  ⬜ To Do
  │    ├─ SRP-24   Create ParsedReport model           ✅ Done
  │    ├─ SRP-25   Create CustomerSection model        ✅ Done
  │    ├─ SRP-26   Create ParsedItem model             ✅ Done
  │    ├─ SRP-27   Create ContinuationRow model        ✅ Done
  │    ├─ SRP-28   Create totals models                ✅ Done
  │    ├─ SRP-29   Implement parser-to-model mapping service ✅ Done
  │    └─ SRP-30   Add persistence tests               ✅ Done
  ├─ SRP-12   Processed Data Retrieval API        ⬜ ← current
  ├─ SRP-13   Basic Dashboard View                ⬜ To Do
  ├─ SRP-14   Error Handling and Validation       ⬜ To Do
  └─ SRP-15   Documentation and Demo Readiness    ⬜ To Do
```
---

## Backlog Order

1. ~~SRP-1 – Initial Project Setup~~ ✅ Done
2. ~~SRP-9 – Django Project and App Scaffold~~ ✅ Done
3. ~~SRP-3 – File Upload API~~ ✅ Done
4. ~~SRP-10 – TXT Parsing Engine~~ ✅ Done
5. SRP-11 – Parsed Data Models
6. SRP-12 – Processed Data Retrieval API  ← current
7. SRP-13 – Basic Dashboard View
8. SRP-14 – Error Handling and Validation
9. SRP-15 – Documentation and Demo Readiness