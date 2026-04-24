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
- SRP-10 (TXT Parsing Engine) is **Done**
- SRP-11 (Parsed Data Models) is **Done**
- SRP-12 (Processed Data Retrieval API) is **Done**
- SRP-13 (Basic Dashboard View) is **Done**

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
- Parsed data models and persistence service implemented
- Retrieval list/detail API is implemented and validated
- Retrieval API tests are implemented and passing
- Initial dashboard route and service layer are implemented and merged for SRP-13
- KPI strip focus for SRP-13:
  - `Pedidos em Atraso` counts unique `pedido + seq` lines with `dt_entr` before today
  - `Produzido Com Data Vencida` sums `sdo_estoq` on overdue rows
  - `Peso em Atraso` uses `qt_ped - qt_fatur - sdo_estoq` on overdue rows
  - `Falta Produzir` uses `qt_ped - qt_fatur - sdo_estoq`
  - `Entrega Esse Mes` uses `qt_ped` for the current month
  - `Saldo em Estoque` uses the current report open balance
  - `Faturado` uses the current report invoiced total
  - `Valor em Pedidos` uses the current report value total
  - `Quantidade Pedida` uses the current report ordered total
  - `Preco Medio` prefers an item-level weighted average when item coverage
    matches report totals, with fallback to `Valor em Pedidos / Quantidade Pedida`
  - `Itens Acionaveis` and `Clientes com Flags` remain out of the main KPI strip for now
- Visao Operacional focus for SRP-13:
  - overdue order-line pressure versus total unique `pedido + seq`
  - overdue remaining demand by client
  - overdue produced stock by client
  - overdue commercial value by client using `pre_liq`
- Current story-driven dashboard flow for SRP-13:
  - `Indicadores Principais`
  - `Visao Operacional`
  - `Excecoes Operacionais`
  - `Fila de Prioridades`
  - `Carteira em Foco`
  - `Clientes em Evidencia`
  - `Cliente 360`
  - `Timeline de Entregas`
- `Fila de Prioridades` is rendered from `worklist_rows` as the main action queue
- `Carteira em Foco` is rendered from `client_rows` with business-priority ordering
- `Cliente 360` now follows the first-ranked `Carteira em Foco` account explicitly
  and explains the handoff from portfolio priority into drilldown context
- Support visibility now uses row-based sections instead of the earlier four-card
  strip:
  - `Excecoes Operacionais`
  - `Clientes em Evidencia`
- Dashboard service and view coverage are implemented and passing locally
- SRP delivery governance is now defined in:
  - `docs/AI/AI_DELIVERY_SYSTEM_SRP.md`
- Backend tests implemented and passing
- Upload endpoint documented in README

### Active Delivery Focus

- Current story: `SRP-15 — Documentation and Demo Readiness`
- Current phase: public showcase packaging in progress
- Prerequisites satisfied:
  - `SRP-12` retrieval endpoints and tests are complete
  - `SRP-13` dashboard flow is implemented, reviewed, merged, and closed
  - `SRP-14` error handling and validation flow is implemented, merged, and closed
- Primary local authority for the finalized SRP-13 dashboard shape:
  - `docs/AI/SRP_13_DASHBOARD_AGREED_SCOPE.md`
- Recent completion:
  - `SRP-39` defined the processing failure contract in Jira
  - `SRP-40` made report persistence atomic
  - `SRP-41` added explicit processing-path validation before persistence
  - `SRP-42` locked endpoint-safe behavior for failure-adjacent states into tests
  - `SRP-43` defined the public-vs-private documentation boundary
  - `SRP-44` added the public run/demo guide
- Current subtask focus: `SRP-45 — Final public repo documentation sync`
- Resume point:
  - apply the public documentation boundary to repo-visible docs
  - reduce or relocate internal-facing project-control surfaces
  - leave the public repo in a clean showcase-ready state

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
- `AI_DELIVERY_SYSTEM_SRP.md` governs ticket sequencing, readiness, and closure workflow
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
7. A basic dashboard displays a story-driven operational flow with summary,
   queue, client focus, drilldown, and supporting detail
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
  ├─ SRP-11   Parsed Data Models                  ✅ Done
  │    ├─ SRP-24   Create ParsedReport model           ✅ Done
  │    ├─ SRP-25   Create CustomerSection model        ✅ Done
  │    ├─ SRP-26   Create ParsedItem model             ✅ Done
  │    ├─ SRP-27   Create ContinuationRow model        ✅ Done
  │    ├─ SRP-28   Create totals models                ✅ Done
  │    ├─ SRP-29   Implement parser-to-model mapping service ✅ Done
  │    └─ SRP-30   Add persistence tests               ✅ Done
  ├─ SRP-12   Processed Data Retrieval API        ✅ Done
  │    ├─ SRP-31   Validate Current Retrieval API Against Story Criteria ✅ Done
  │    ├─ SRP-32   Complete Retrieval API Behavior Gaps ✅ Done
  │    ├─ SRP-33   Add or Update Retrieval API Tests   ✅ Done
  │    └─ SRP-34   Sync SRP-12 Delivery State and Docs ✅ Done
  ├─ SRP-13   Basic Dashboard View                ✅ Done
  ├─ SRP-14   Error Handling and Validation       ✅ Done
  │    ├─ SRP-39   Define processing failure contract ✅ Done
  │    ├─ SRP-40   Make report persistence atomic ✅ Done
  │    ├─ SRP-41   Implement explicit validation and error handling for processing path ✅ Done
  │    └─ SRP-42   Validate endpoint failure states and sync tests ✅ Done
  └─ SRP-15   Documentation and Demo Readiness    ⬜ ← next
```
---

## Backlog Order

1. ~~SRP-1 – Initial Project Setup~~ ✅ Done
2. ~~SRP-9 – Django Project and App Scaffold~~ ✅ Done
3. ~~SRP-3 – File Upload API~~ ✅ Done
4. ~~SRP-10 – TXT Parsing Engine~~ ✅ Done
5. ~~SRP-11 – Parsed Data Models~~ ✅ Done
6. ~~SRP-12 – Processed Data Retrieval API~~ ✅ Done
7. ~~SRP-13 – Basic Dashboard View~~ ✅ Done
8. ~~SRP-14 – Error Handling and Validation~~ ✅ Done
9. SRP-15 – Documentation and Demo Readiness  ← next
