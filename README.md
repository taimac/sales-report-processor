# Sales Report Processor

Sales Report Processor is a Django-based MVP that transforms supplier TXT/PDF
reports into structured data and exposes that information through a retrieval
API and a story-driven operational dashboard.

The project is based on a real B2B industrial sales workflow where report
processing is often manual, slow, and difficult to turn into actionable
follow-up priorities.

## What It Solves

Supplier reports typically arrive as raw operational files containing:

- production updates
- delivery dates
- quantities and balances
- commercial references

In many sales teams, this information is processed manually before anyone can
decide what needs attention first. SRP reduces that gap by turning raw report
content into a structured operational view.

## MVP Capabilities

- upload TXT and PDF files through `POST /api/reports/upload/`
- validate file presence and supported extension
- parse TXT reports into structured business fields
- persist structured report, customer, item, continuation, and total records
- expose processed data through:
  - `GET /api/reports/`
  - `GET /api/reports/{id}/`
- render the latest processed report at `GET /dashboard/`
- fail safely around invalid processing input and incomplete related data

## Dashboard Flow

The dashboard is designed as an action-oriented operational page, not just a
summary screen.

Current flow:

- `Indicadores Principais`
- `Visao Operacional`
- `Excecoes Operacionais`
- `Fila de Prioridades`
- `Carteira em Foco`
- `Clientes em Evidencia`
- `Cliente 360`
- `Timeline de Entregas`

## Public Docs

- Demo walkthrough:
  [docs/demo_guide.md](docs/demo_guide.md)
- Architecture and design overview:
  [docs/architecture_overview.md](docs/architecture_overview.md)

This public repository is intentionally focused on the product, architecture,
and demo surface. Internal workflow-control and AI operating documents are
maintained separately in a private continuation workspace.

## Quick Start

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the local environment file:

```bash
cp .env.example .env
```

Run the backend:

```bash
cd backend
python manage.py runserver
```

If your local `.env` carries a non-boolean `DEBUG` value, run Django commands
with:

```bash
env DEBUG=True python manage.py runserver
```

For the complete public setup-to-demo flow, use
[docs/demo_guide.md](docs/demo_guide.md).

## Validation

Focused MVP validation command:

```bash
env DEBUG=True venv/bin/python backend/manage.py test reports.tests.test_upload_api reports.tests.test_retrieval_api reports.tests.test_dashboard_view reports.tests.test_persistence
```

## Tech Stack

- Backend: Django + Django REST Framework
- Database: SQLite for MVP
- Parsing: Python text processing
- Frontend: server-rendered Django templates
- Python: 3.12

## Repository Structure

```text
sales-report-processor/
├── backend/
│   ├── manage.py
│   ├── reports/
│   └── srp/
├── docs/
│   ├── architecture_overview.md
│   └── demo_guide.md
├── requirements.txt
├── .env.example
└── README.md
```

## Engineering Approach

This project was built with an emphasis on:

- business-driven software design
- clear separation between parsing, persistence, API, and dashboard layers
- test coverage for behavior-changing work
- MVP discipline over premature complexity

## Current Limits

- advanced PDF parsing is not implemented
- no authentication or user management
- no async processing or background jobs
- no deployment packaging or Docker workflow yet
- no advanced SPA frontend

## Why This Project Matters

SRP is intended as a practical showcase of business-aware software work:

- turning messy operational inputs into structured information
- connecting backend processing to daily decision-making
- designing software around real commercial use cases instead of toy data

## Author

Tailor Maciel  
Business + Data + Systems Builder
