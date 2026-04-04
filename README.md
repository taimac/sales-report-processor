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
- Basic dashboard (summary + table view)

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

## Project Structure

```
sales-report-processor/
├── backend/                  ← Django project (API + processing)
├── frontend/                 ← basic dashboard (MVP) / React SPA (future)
├── docs/
│   ├── AI/                   ← AI system documentation
│   │   ├── AI_CONTEXT_SRP.md
│   │   ├── AI_OS_SRP.md
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

### Current Focus
- SRP-9 — Django Project and App Scaffold

---

## Example Use Case

1. Upload supplier report (TXT/PDF)
2. System validates and stores the file
3. System parses key data from TXT reports
4. Structured data is saved in the database
5. Dashboard displays:
   - total reports processed
   - number of records extracted
   - status distribution
   - table of extracted data

---

## How to Run

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

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

To export backlog:

```bash
python fetch_jira_backlog_srp.py
```

Output:

```
docs/jira_backlog_SRP.md
```

---

## Development Roadmap (MVP)

The MVP is structured into a clear sequence of deliverable stories, ensuring incremental progress and a working system at each stage.

### Story Breakdown

- **SRP-1 — Initial Project Setup** ✅
  Repository, environment, dependencies, and baseline structure.

- **SRP-9 — Django Project and App Scaffold** ← current
  Base Django project and application setup required for backend implementation.

- **SRP-3 — File Upload API**
  Endpoint to receive, validate, and store TXT/PDF reports.

- **SRP-10 — TXT Parsing Engine**
  Initial parsing logic to extract structured fields from TXT reports.

- **SRP-11 — Parsed Data Models**
  Database models to store extracted report data.

- **SRP-12 — Processed Data Retrieval API**
  API endpoints to expose structured data for consumption.

- **SRP-13 — Basic Dashboard View**
  Simple interface to display summarised data and extracted records.

- **SRP-14 — Error Handling and Validation**
  Improve robustness through validation and consistent error responses.

- **SRP-15 — Documentation and Demo Readiness**
  Finalise documentation and prepare the project for presentation.

---

## Execution Strategy

The project follows a **backend-first approach**, ensuring that core functionality is stable before adding presentation layers.

Each stage builds on the previous one, progressively delivering:

1. Data ingestion (upload)
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