# Sales Report Processor (MVP)

## Overview

Sales Report Processor is a backend-driven MVP designed to transform unstructured supplier reports (TXT/PDF) into structured data and present actionable insights through a simple dashboard.

This project is based on real workflows in B2B industrial sales, where report processing is often manual, time-consuming, and limits visibility for decision-making.

---

## Problem

Sales representatives frequently receive supplier reports in TXT or PDF formats containing:

- invoice data
- production updates
- delivery status

These reports are:

- unstructured
- manually processed
- difficult to analyze quickly

This leads to:

- delayed decisions
- lack of operational visibility
- inefficient follow-up actions

---

## Solution

This system provides an end-to-end pipeline:

- upload supplier reports (TXT/PDF)
- extract key business data (TXT parsing — initial phase)
- store structured information
- present summarized insights via a basic dashboard

The goal is to transform raw operational data into usable business intelligence.

---

## MVP Scope

### Included

- Upload TXT/PDF reports via API
- File validation (type and presence)
- TXT parsing engine (initial version)
- Extraction of key fields:
  - order number
  - client
  - product
  - quantity
  - status
- Structured data storage
- API to retrieve processed data
- Basic dashboard with story-driven operational sections

### Not Included (Future Phases)

- Advanced PDF parsing (complex layouts)
- Authentication / user management
- Browser automation
- Advanced frontend (React SPA)
- Machine learning / predictive analytics
- Full SalesApp integration
- Docker setup

---

## Tech Stack

- **Backend:** Python (Django / Django REST Framework)
- **Database:** SQLite (MVP) → PostgreSQL (production)
- **Parsing:** Python (regex / text processing)
- **Frontend (MVP):** Simple server-rendered view or minimal interface
- **Environment:** Local (Docker planned)

---

## Engineering Standards

This project follows a lightweight but explicit software lifecycle discipline:

- design before building when a feature introduces new structure or flow
- separation of concerns between view, service, persistence, parsing, and presentation layers
- high cohesion inside modules
- loose coupling between layers
- security-first defaults and validation
- tests for behavior-changing work
- documentation updates as part of implementation closure

These standards apply even when SRP remains MVP-simple.

---

## Project Structure

```
sales-report-processor/
├── backend/                  ← Django project (API + processing)
├── frontend/                 ← basic dashboard (MVP) / React SPA (future)
├── docs/
│   ├── AI/                   ← AI system documentation
│   │   ├── AI_CONTEXT_SRP.md
│   │   ├── AI_OS_SRP.md
│   │   ├── AI_DELIVERY_SYSTEM_SRP.md
│   │   ├── AI_DECISION_RULES_SRP.md
│   │   ├── AI_RUNTIME_LOOP_SRP.md
│   │   ├── AI_OUTPUT_CONTRACTS_SRP.md
│   │   └── AI_BOOTSTRAP_PROMPT_SRP.md
│   ├── jira_backlog_SRP.md
│   └── project_instructions_SRP.md
├── fetch_jira_backlog_srp.py
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

---

## Current Status

🚧 MVP in development

### Done
- SRP-1 — Initial Project Setup ✅
- SRP-9 — Django Project and App Scaffold ✅
- SRP-4 — UploadedReport model ✅
- SRP-5 — Upload API endpoint ✅
- SRP-6 — File validation (TXT/PDF) ✅
- SRP-7 — Backend tests for upload endpoint ✅
- SRP-8 — Upload endpoint documentation ✅
- SRP-10 — TXT Parsing Engine ✅
- SRP-11 — Parsed Data Models ✅
- SRP-12 — Processed Data Retrieval API ✅

### Current Focus
- SRP-13 — Basic Dashboard View

### Active Delivery Work
- reconcile local delivery-state docs after the implemented SRP-13 dashboard flow
- package the dashboard path for the next ticket transition

### Delivery Governance
- Project-level delivery control now lives in `docs/AI/AI_DELIVERY_SYSTEM_SRP.md`
- Ticket sequencing and readiness are resolved from Jira backlog authority first, then validated against local codebase truth
- `SRP-12` is complete and `SRP-13` is implemented locally, with backlog/state synchronization still pending

### Dashboard Snapshot
- `GET /dashboard/` renders the latest parsed report using a server-rendered,
  story-driven operational layout
- The current dashboard flow is:
  - `Indicadores Principais`
  - `Visao Operacional`
  - `Excecoes Operacionais`
  - `Fila de Prioridades`
  - `Carteira em Foco`
  - `Clientes em Evidencia`
  - `Cliente 360`
  - `Timeline de Entregas`
- `Fila de Prioridades` is the main action surface
- `Carteira em Foco` ranks accounts by business priority
- `Cliente 360` drills into the first-ranked account from `Carteira em Foco`
- Dashboard service and view tests pass locally
---

## Example Use Case

1. Upload supplier report (TXT/PDF)
2. System validates and stores the file
3. System parses key data from TXT reports
4. Structured data is saved in the database
5. Dashboard displays:
   - top operational KPIs
   - operational pressure views
   - priority queue for immediate follow-up
   - client-priority portfolio ranking
   - account drilldown for the top focused client
   - supporting delivery and exception detail

---

## How to Run

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

## Upload Reports API

### Endpoint

```
POST /api/reports/upload/
```

---

### Description

Uploads a supplier report file (TXT or PDF), stores it on disk, and registers it in the system for further processing.

---

### Request

**Content-Type:** `multipart/form-data`

**Form field:**

| Field | Type | Required | Description |
|------|------|----------|-------------|
| file | File | Yes | TXT or PDF report file |

---

### Example (curl)

```bash
curl -X POST http://127.0.0.1:8000/api/reports/upload/ \
  -F "file=@sample_report.txt"
```

### Success Response

```
Status: 201 Created
```

``` 
{
  "id": 1,
  "file": "reports/sample_report.txt",
  "uploaded_at": "2026-04-06T14:00:57.996088Z",
  "message": "File uploaded successfully."
}
```

#### Error Responses

Missing file

``` 
Status: 400 Bad Request
```

```
{
  "error": "No file provided."
}
```

#### Unsupported file type

```
Status: 400 Bad Request
```

```
{
  "error": "Unsupported file type. Only .txt and .pdf files are allowed."
}
```

### Notes

- Files are stored under:

```
backend/media/reports/
```

- The database stores only the file path, not the file content
- Duplicate filenames are automatically handled by Django (unique suffix added)
- Validation is extension-based only (MVP scope)

### Supported File Types:
- .txt → accepted
- .pdf → accepted
- others → rejected

## Processed Reports API

### Endpoints

```
GET /api/reports/
GET /api/reports/{id}/
```

### Purpose

Return persisted processed report data for API consumers and the future MVP dashboard.

### Delivery Note

The retrieval layer is complete under `SRP-12` and has passing backend coverage.
Current delivery work now moves to `SRP-13`, where the MVP dashboard will consume the validated retrieval API.

## Dashboard

### Endpoint

```
GET /dashboard/
```

### Purpose

Render the latest processed report as a daily sales action dashboard with:

- top KPI strip
- operational charts for overdue pressure, overdue stock, and value at risk
- client portfolio table
- order/material worklist

### KPI Rules

The principal indicators are aligned to wallet and delivery management:

- `Pedidos em Atraso` counts unique `pedido + seq` lines where `dt_entr` is before today
- `Produzido Com Data Vencida` sums `sdo_estoq` for overdue rows
- `Peso em Atraso` uses the same remaining-to-produce formula, but only for overdue rows
- `Falta Produzir` uses `qt_ped - qt_fatur - sdo_estoq`
- `Entrega Esse Mes` uses `qt_ped` for rows whose `dt_entr` falls in the current month
- `Saldo em Estoque` uses the current report open balance
- `Faturado` uses the current report invoiced total
- `Valor em Pedidos` uses the current report value total
- `Quantidade Pedida` uses the current report ordered total
- `Preco Medio` uses `Valor em Pedidos / Quantidade Pedida`
- the noisy `Itens Acionaveis` and `Clientes com Flags` counters are intentionally kept out of the principal KPI strip for now

### Visao Operacional

The operational board is chart-led and answers four questions:

- how many order lines are overdue relative to the full report line count
- which clients concentrate delayed remaining demand
- which clients already hold produced stock with overdue delivery dates
- which clients concentrate overdue commercial value, split between produced overdue stock and delayed remaining demand

### Data Source

- Uses the latest persisted `ParsedReport`
- Queries Django models directly
- Does not call the API over HTTP internally

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Update environment variables if needed
```

### 4. Run backend

```bash
cd backend
python manage.py runserver
```

---

## Jira Integration

This project uses Jira for backlog tracking and planning.

Project-level ticket governance is defined in:

```text
docs/AI/AI_DELIVERY_SYSTEM_SRP.md
```

To export backlog:

```bash
python fetch_jira_backlog_srp.py
```

Output:

```
docs/jira_backlog_SRP.md
```

### Ticket Workflow Automation

To automate the post-ticket workflow:

- push feature branch
- optionally create PR
- close current Jira ticket with a comment
- derive the next ticket from the ordered Jira backlog and move it to In Progress
- refresh `docs/jira_backlog_SRP.md`
- update `docs/AI/AI_CONTEXT_SRP.md`
- commit the refreshed docs
- merge the PR
- sync `dev`
- optionally delete the merged feature branch

`docs/jira_backlog_SRP.md` now includes an `Execution Order` section with explicit
parent/subtask relationships. The workflow script uses that section as the source
of truth for automated decisions.

Dry run:

```bash
./venv/bin/python complete_ticket_workflow.py \
  --current-ticket SRP-30 \
  --jira-comment "Completed SRP-30. Persistence flow is covered by tests." \
  --dry-run
```

Real run:

```bash
./venv/bin/python complete_ticket_workflow.py \
  --current-ticket SRP-30 \
  --jira-comment "Completed SRP-30. Persistence flow is covered by tests." \
  --create-pr \
  --delete-branch
```

---

## Development Roadmap (MVP)

The MVP is structured into a clear sequence of deliverable stories, ensuring incremental progress and a working system at each stage.

### Story Breakdown

- **SRP-1 — Initial Project Setup** ✅
  Repository, environment, dependencies, and baseline structure.

- **SRP-9 — Django Project and App Scaffold** ✅
  Base Django project and application setup required for backend implementation.

- **SRP-3 — File Upload API** ✅
  Endpoint to receive, validate, and store TXT/PDF reports.

- **SRP-10 — TXT Parsing Engine**
  Initial parsing logic to extract structured fields from TXT reports. ✅

- **SRP-11 — Parsed Data Models**
  Database models and persistence layer to store extracted report data. ✅

- **SRP-12 — Processed Data Retrieval API** ✅
  Retrieval endpoints, serializers, and tests are implemented and validated.

- **SRP-13 — Basic Dashboard View**
  Active story. Current implementation direction is an action-oriented dashboard for sales follow-up, client priority, and operational worklist visibility.

- **SRP-14 — Error Handling and Validation**
  Improve robustness through validation and consistent error responses.

- **SRP-15 — Documentation and Demo Readiness**
  Finalise documentation and prepare the project for presentation.

---

## Execution Strategy

The project follows a **backend-first approach**, ensuring that core functionality is stable before adding presentation layers.

Each stage builds on the previous one, progressively delivering:

1. Data ingestion (upload via API)
2. Data processing (parsing)
3. Data structuring (models)
4. Data exposure (API)
5. Data visualisation (dashboard)

This approach ensures that the system delivers real value early while remaining simple and maintainable.

---

## Why This Project Matters

This project focuses on solving a real operational bottleneck in B2B sales environments:

- transforming unstructured reports into structured data
- reducing manual processing effort
- improving speed and quality of decision-making

It reflects a practical approach where business understanding directly drives software design.

---

## Author

Tailor Maciel

Business + Data + Systems Builder
B2B Sales (20+ years) → Data Science & Software Engineering

---

## Vision

This project is part of a broader system (SalesApp) aimed at:

- automating commercial workflows
- enhancing decision-making with data
- connecting business operations with intelligent systems

The long-term goal is to provide sales representatives with real-time insights, automation, and predictive capabilities.
