# Sales Report Processor (MVP)

## Overview

Sales Report Processor is a backend-focused MVP designed to transform unstructured supplier reports (TXT/PDF) into structured data for sales and operational decision-making.

This project is based on real workflows in B2B industrial sales, where report processing is often manual, time-consuming, and error-prone.

---

## Problem

Sales representatives frequently receive supplier reports in TXT or PDF formats containing:

* invoice data
* production updates
* delivery status

These reports are:

* unstructured
* manually processed
* difficult to analyze quickly

This leads to:

* delayed decisions
* lack of visibility
* operational inefficiencies

---

## Solution

This system provides:

* file upload (TXT/PDF)
* data extraction (parsing engine)
* structured storage
* API access to processed data

The goal is to convert raw operational data into usable business insights.

---

## MVP Scope

### Included

* Upload TXT/PDF reports via API
* Basic validation (file type)
* Store uploaded files
* Prepare structure for parsing engine
* Expose data through API endpoints

### Not Included (yet)

* Authentication
* Browser automation
* Advanced UI
* Machine learning / predictions

---

## Tech Stack

* **Backend:** Python (Django / Django REST Framework)
* **Database:** PostgreSQL
* **Parsing:** Python (regex / PDF parsing libraries)
* **Environment:** Local (Docker planned)

---

## Project Structure

```
sales-report-processor/
│
├── backend/
├── frontend/        # planned
├── docs/
│   ├── AI/          # AI system (lightweight)
│   └── jira_backlog_SRP.md
├── fetch_jira_backlog_srp.py
├── requirements.txt
└── README.md
```

---

## Current Status

🚧 MVP in development

### Current Focus

* SRP-2 — File Upload API

---

## Example Use Case

1. Upload supplier report (TXT/PDF)
2. System stores file
3. (Next step) parse key data:

   * order number
   * client
   * product
   * quantity
   * status
4. Expose structured data via API

---

## How to Run

### 1. Create virtual environment

```
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run backend (planned)

```
python manage.py runserver
```

---

## Jira Integration

This project integrates with Jira for backlog tracking.

To export backlog:

```
python fetch_jira_backlog_srp.py
```

Output:

```
docs/jira_backlog_SRP.md
```

---

## Author

Tailor Maciel

Business + Data + Systems Builder
B2B Sales (20+ years) → Data Science & Software Engineering

---

## Vision

This project is part of a broader system (SalesApp) aimed at:

* automating commercial processes
* improving decision-making with data
* connecting business operations with software

The long-term goal is to build intelligent systems that support sales representatives with real-time insights and automation.
