<!--
Purpose: Public setup, validation, and demo guide for the SRP MVP.
Date: 2026-04-24
Author: Codex
Domain: Systems / SRP
-->

# SRP Demo Guide

## Purpose

Use this guide to run the Sales Report Processor MVP locally and walk through its
main capabilities from an external-reader perspective.

This demo path is intentionally simple:

1. set up the local environment
2. start the backend
3. verify file upload
4. seed one minimal parsed report for public demo purposes
5. inspect retrieval endpoints
6. inspect the dashboard
7. run one focused validation command

## Before You Start

- Python 3.12 installed
- terminal access
- repo cloned locally

The commands below assume you are at the project root:

```bash
cd sales-report-processor
```

## 1. Set Up The Environment

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

If your local `.env` carries a non-boolean `DEBUG` value, use `DEBUG=True`
when running Django commands locally.

## 2. Start The Backend

From the project root:

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

If needed:

```bash
cd backend
env DEBUG=True python manage.py migrate
env DEBUG=True python manage.py runserver
```

The app will be available at:

- `http://127.0.0.1:8000/api/reports/upload/`
- `http://127.0.0.1:8000/api/reports/`
- `http://127.0.0.1:8000/dashboard/`

## 3. Verify File Upload

In a second terminal, from the project root:

Create a small local TXT file for the upload check:

```bash
printf "Sample TXT content\n" > /tmp/srp-demo-upload.txt
```

```bash
curl -X POST http://127.0.0.1:8000/api/reports/upload/ \
  -F "file=@/tmp/srp-demo-upload.txt"
```

Expected result:

- `201 Created`
- response contains `id`, `file`, `uploaded_at`, and `message`

What this proves:

- the upload endpoint accepts TXT files
- the file is stored under `backend/media/reports/`

## 4. Seed A Minimal Parsed Report

The current MVP exposes upload and processed-data retrieval as separate
capabilities, and the public repo does not yet ship a tracked supplier fixture
for parser-driven persistence. To keep the public demo reproducible on a clean
checkout, seed one minimal parsed report with Django shell:

```bash
env DEBUG=True venv/bin/python backend/manage.py shell -c "from reports.models import UploadedReport, ParsedReport, ReportTotal; uploaded = UploadedReport.objects.create(file='reports/demo-seeded.txt'); parsed = ParsedReport.objects.create(uploaded_report=uploaded, generated_date='24/04/2026', generated_time='10:00:00'); ReportTotal.objects.create(parsed_report=parsed, total_ped='100', total_in_prod='60', total_fatur='20', total_sdo='20', total_valor='1000,00'); print(parsed.id)"
```

Expected result:

- the command prints a parsed report id, such as `8`

Keep that id for the next step.

## 5. Inspect The Retrieval API

List parsed reports:

```bash
curl http://127.0.0.1:8000/api/reports/
```

Inspect the specific parsed report created in the previous step:

```bash
curl http://127.0.0.1:8000/api/reports/<parsed_report_id>/
```

Expected result:

- list endpoint returns persisted parsed reports
- detail endpoint returns the nested structured payload for one report

## 6. Inspect The Dashboard

Open in your browser:

```text
http://127.0.0.1:8000/dashboard/
```

Expected result:

- the latest persisted parsed report renders as the operational dashboard
- story flow includes:
  - `Indicadores Principais`
  - `Visao Operacional`
  - `Excecoes Operacionais`
  - `Fila de Prioridades`
  - `Carteira em Foco`
  - `Clientes em Evidencia`
  - `Cliente 360`
  - `Timeline de Entregas`

## 7. Run One Validation Command

From the project root:

```bash
env DEBUG=True venv/bin/python backend/manage.py test reports.tests.test_upload_api reports.tests.test_retrieval_api reports.tests.test_dashboard_view reports.tests.test_persistence
```

This validates the main MVP paths covered by:

- upload behavior
- retrieval behavior
- dashboard rendering
- persistence and rollback rules

## Demo Notes

- The upload endpoint stores raw files only
- The public demo seeds a minimal `ParsedReport` through Django shell so the
  retrieval API and dashboard can be exercised on a clean checkout
- Dashboard and retrieval operate on the latest persisted `ParsedReport`

## Current MVP Limits

- PDF upload is accepted, but advanced PDF parsing is not implemented
- authentication is not part of the MVP
- no async processing or background jobs
- no deployment packaging or Docker workflow yet
