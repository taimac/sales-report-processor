# Jira Backlog for Project SRP
_Exported: 2026-04-12 01:30:33_

**Total Issues:** 30

## Execution Order

This section is the source of truth for workflow automation. It preserves Jira rank order and makes story/subtask hierarchy explicit.

| Order | Level | Key | Parent | Summary | Status | Sprint |
|-------|-------|-----|--------|---------|--------|--------|
| 1 | story | SRP-1 | SRP-2 | Initial Project Setup | Done | No Sprint |
| 2 | story | SRP-2 |  | Sales Report Processor MVP | To Do | No Sprint |
| 3 | story | SRP-9 | SRP-2 | Django Project and App Scaffold | Done | SRP Sprint 1 |
| 4 | story | SRP-3 | SRP-2 | File Upload API | Done | SRP Sprint 1 |
| 5 | subtask | SRP-4 | SRP-3 | Create upload data model | Done | SRP Sprint 1 |
| 6 | subtask | SRP-5 | SRP-3 | Implement upload API endpoint | Done | SRP Sprint 1 |
| 7 | subtask | SRP-6 | SRP-3 | Add file validation for TXT/PDF uploads | Done | SRP Sprint 1 |
| 8 | subtask | SRP-7 | SRP-3 | Add backend tests for upload endpoint | Done | SRP Sprint 1 |
| 9 | subtask | SRP-8 | SRP-3 | Document upload endpoint behavior | Done | SRP Sprint 1 |
| 10 | story | SRP-10 | SRP-2 | TXT Parsing Engine | Done | SRP Sprint 2 |
| 11 | story | SRP-11 | SRP-2 | Parsed Data Models | In Progress | SRP Sprint 2 |
| 12 | story | SRP-12 | SRP-2 | Processed Data Retrieval API | To Do | SRP Sprint 3 |
| 13 | story | SRP-13 | SRP-2 | Basic Dashboard View | To Do | SRP Sprint 3 |
| 14 | story | SRP-14 | SRP-2 | Error Handling and Validation | To Do | SRP Sprint 4 |
| 15 | story | SRP-15 | SRP-2 | Documentation and Demo Readiness | To Do | SRP Sprint 4 |
| 16 | subtask | SRP-16 | SRP-10 | TXT Reader and Header Metadata Extraction | Done | SRP Sprint 2 |
| 17 | subtask | SRP-17 | SRP-10 | Line Classification and Report Structure Detection | Done | SRP Sprint 2 |
| 18 | subtask | SRP-18 | SRP-10 | Parse Production, Delivery, and Quantity Columns | Done | SRP Sprint 2 |
| 19 | subtask | SRP-19 | SRP-10 | Parse Commercial, Credit, and Reference Columns | Done | SRP Sprint 2 |
| 20 | subtask | SRP-20 | SRP-10 | Continuation Row Parsing and Parent Item Attachment | Done | SRP Sprint 2 |
| 21 | subtask | SRP-21 | SRP-10 | Client and Grand Total Extraction | Done | SRP Sprint 2 |
| 22 | subtask | SRP-22 | SRP-10 | Final Parser Assembly and Real Sample Tests | Done | SRP Sprint 2 |
| 23 | subtask | SRP-23 | SRP-10 | Parse Core Main Row Identity and Product Columns | Done | SRP Sprint 2 |
| 24 | subtask | SRP-24 | SRP-11 | Create ParsedReport model | Done | SRP Sprint 2 |
| 25 | subtask | SRP-25 | SRP-11 | Create CustomerSection model | Done | SRP Sprint 2 |
| 26 | subtask | SRP-26 | SRP-11 | Create ParsedItem model | Done | SRP Sprint 2 |
| 27 | subtask | SRP-27 | SRP-11 | Create ContinuationRow model | Done | SRP Sprint 2 |
| 28 | subtask | SRP-28 | SRP-11 | Create totals models | Done | SRP Sprint 2 |
| 29 | subtask | SRP-29 | SRP-11 | Implement parser-to-model mapping service | Done | SRP Sprint 2 |
| 30 | subtask | SRP-30 | SRP-11 | Add persistence tests | Done | SRP Sprint 2 |

## Hierarchy

- SRP-2 — Sales Report Processor MVP [To Do]
  - SRP-1 — Initial Project Setup [Done]
  - SRP-9 — Django Project and App Scaffold [Done]
  - SRP-3 — File Upload API [Done]
    - SRP-4 — Create upload data model [Done]
    - SRP-5 — Implement upload API endpoint [Done]
    - SRP-6 — Add file validation for TXT/PDF uploads [Done]
    - SRP-7 — Add backend tests for upload endpoint [Done]
    - SRP-8 — Document upload endpoint behavior [Done]
  - SRP-10 — TXT Parsing Engine [Done]
    - SRP-16 — TXT Reader and Header Metadata Extraction [Done]
    - SRP-17 — Line Classification and Report Structure Detection [Done]
    - SRP-18 — Parse Production, Delivery, and Quantity Columns [Done]
    - SRP-19 — Parse Commercial, Credit, and Reference Columns [Done]
    - SRP-20 — Continuation Row Parsing and Parent Item Attachment [Done]
    - SRP-21 — Client and Grand Total Extraction [Done]
    - SRP-22 — Final Parser Assembly and Real Sample Tests [Done]
    - SRP-23 — Parse Core Main Row Identity and Product Columns [Done]
  - SRP-11 — Parsed Data Models [In Progress]
    - SRP-24 — Create ParsedReport model [Done]
    - SRP-25 — Create CustomerSection model [Done]
    - SRP-26 — Create ParsedItem model [Done]
    - SRP-27 — Create ContinuationRow model [Done]
    - SRP-28 — Create totals models [Done]
    - SRP-29 — Implement parser-to-model mapping service [Done]
    - SRP-30 — Add persistence tests [Done]
  - SRP-12 — Processed Data Retrieval API [To Do]
  - SRP-13 — Basic Dashboard View [To Do]
  - SRP-14 — Error Handling and Validation [To Do]
  - SRP-15 — Documentation and Demo Readiness [To Do]

---

## Summary

- **To Do:** 5 issues
- **In Progress:** 1 issues
- **Done:** 24 issues

---

## To Do (5 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-2 | Sales Report Processor MVP | To Do | 2026-04-04 | 2026-04-04 | No Sprint |
| SRP-12 | Processed Data Retrieval API | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 3 |
| SRP-13 | Basic Dashboard View | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 3 |
| SRP-14 | Error Handling and Validation | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 4 |
| SRP-15 | Documentation and Demo Readiness | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 4 |

### SRP-2 – Sales Report Processor MVP

- **Status:** To Do
- **Type:** Story
- **Parent:** —
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** No Sprint

**Description**

The Sales Report Processor MVP is a backend-focused system designed to transform unstructured supplier reports (TXT/PDF) into structured data that can be used for sales tracking, operational monitoring, and decision-making.

This project is inspired by real-world workflows in B2B industrial sales, where supplier reports are manually processed, leading to inefficiencies, delays, and lack of visibility.

The MVP aims to deliver a minimal but functional pipeline that:

* accepts report uploads
* extracts relevant business data
* stores structured information
* exposes data via API

This Epic represents a *self-contained module* that can later integrate into the broader SalesApp ecosystem.

----

## Goal

Deliver a working backend system that:

* processes TXT/PDF supplier reports
* converts unstructured data into structured format
* exposes data for consumption via API

The focus is on *functionality and clarity*, not completeness.

----

## Scope

### Included

* File upload via API (TXT/PDF)
* Basic file validation
* Parsing engine (starting with TXT)
* Extraction of key fields:
** order number
** client
** product
** quantity
** status
* Database storage of parsed data
* API endpoints to retrieve processed data
* Basic error handling

----

### Not Included

* Authentication / user management
* Frontend UI (React)
* Browser automation / extensions
* Advanced parsing (complex PDF edge cases)
* Machine learning / predictive analytics
* Full integration with SalesApp

----

## Business Context

In real B2B sales operations:

* supplier reports are frequently delivered in TXT/PDF formats
* data must be manually extracted and interpreted
* decision-making is delayed due to lack of structured visibility

This MVP addresses this problem by:

{quote}transforming raw operational data into structured, actionable information{quote}

----

## Architecture Direction

* Backend-first approach
* API-driven design
* Modular structure (preparing for future integration)
* Simple and maintainable implementation

----

## Success Criteria

* User can upload a TXT or PDF report
* System validates and stores the file
* System extracts key data from TXT reports
* Extracted data is stored in structured format
* Data can be retrieved via API
* System handles invalid input gracefully

----

## Related Stories

* SRP-1 — Initial Project Setup
* SRP-2 — File Upload API
* SRP-3 — Report Parsing Engine (TXT)
* SRP-4 — Database Models for Parsed Data
* SRP-5 — API to Retrieve Processed Reports
* SRP-6 — Error Handling & Validation
* SRP-7 — Documentation & README

----

## Notes

* This Epic is intentionally *MVP-scoped* and time-boxed
* Avoid over-engineering or premature optimization
* Focus on delivering a working end-to-end flow
* Treat this as a *foundation module* for future expansion

**Comments**

_No comments_

---

### SRP-12 – Processed Data Retrieval API

- **Status:** To Do
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 3

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-13 – Basic Dashboard View

- **Status:** To Do
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 3

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-14 – Error Handling and Validation

- **Status:** To Do
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 4

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-15 – Documentation and Demo Readiness

- **Status:** To Do
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 4

**Description**

_No content_

**Comments**

_No comments_

---

## In Progress (1 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-11 | Parsed Data Models | In Progress | 2026-04-04 | 2026-04-07 | SRP Sprint 2 |

### SRP-11 – Parsed Data Models

- **Status:** In Progress
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Implement database models to persist structured data produced by the TXT parsing engine (SRP-10).

This story introduces the data layer of the Sales Report Processor MVP, enabling parsed report data to be stored in SQLite and later retrieved via API.

The models must reflect the hierarchical structure of the parsed report, including:

* report metadata
* customer sections
* parsed items (main rows)
* continuation rows
* totals

The goal is to transform the in-memory parsed output into a *persistent, queryable dataset*, forming the foundation for SRP-12 (API retrieval) and SRP-13 (dashboard).

----

### *Goal*

Enable the system to store parsed TXT report data in a structured relational format, preserving hierarchy and supporting future API access.

----

### *Context*

SRP-10 delivers a fully functional parsing engine that converts raw TXT reports into structured Python data.

However, this data currently exists only in memory.

To complete the MVP pipeline, the system must:

* persist parsed data in the database
* maintain relationships between report → customers → items → continuations
* support efficient querying and retrieval

This story bridges the gap between parsing and API exposure.

----

### *Scope*

#### *Included*

* Create database models for parsed report data
* Store:
** report metadata (generated date/time, file reference)
** customer sections (representative, customer name)
** parsed items (full row data)
** continuation rows (linked to parent item)
** totals (client-level and global)
* Establish relationships:
** ParsedReport → CustomerSection (1:N)
** CustomerSection → ParsedItem (1:N)
** ParsedItem → ContinuationRow (1:N)
* Link parsed data to uploaded file (`UploadedReport`)
* Create Django migrations
* Ensure compatibility with SRP-22 output structure

----

#### *Not Included*

* API endpoints (SRP-12)
* Frontend/dashboard (SRP-13)
* Advanced normalization or optimization
* Complex indexing or performance tuning

----

### *Proposed Model Structure (MVP-level)*

* *ParsedReport*
** FK → UploadedReport
** generated_date
** generated_time
* *CustomerSection*
** FK → ParsedReport
** representative
** customer_name
* *ParsedItem*
** FK → CustomerSection
** All parsed fields from SRP-23/18/19
* *ContinuationRow*
** FK → ParsedItem
** ord_prod
** sit_ordem
** qt_prod
** sit
* *Totals (optional design choice)*
** Either:
*** separate model
*** or JSON field on CustomerSection / ParsedReport

----

### *Acceptance Criteria*

* Parsed report structure can be saved into the database
* Relationships between report, customers, items, and continuations are preserved
* Data from SRP-22 output maps correctly to models
* Migrations run successfully
* Data can be queried via Django ORM
* No data loss from parsed structure

----

### *Definition of Done*

* Models implemented in `reports/models.py`
* Migrations created and applied
* Sample parsed report successfully stored in DB
* Relationships verified (via shell or tests)
* Code follows project conventions (clean, readable, minimal complexity)

----

### *Notes*

* Keep the model design simple (MVP-first approach)
* Avoid over-normalization or premature optimization
* Preserve flexibility for future API and analytics layers
* This story enables SRP-12 (Processed Data Retrieval API)

----

### *Dependencies*

* SRP-10 — TXT Parsing Engine (completed)
* SRP-3 — File Upload API (provides UploadedReport)

**Comments**

_No comments_

---

## Done (24 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-1 | Initial Project Setup | Done | 2026-04-04 | 2026-04-04 | No Sprint |
| SRP-9 | Django Project and App Scaffold | Done | 2026-04-04 | 2026-04-04 | SRP Sprint 1 |
| SRP-3 | File Upload API | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-4 | Create upload data model | Done | 2026-04-04 | 2026-04-05 | SRP Sprint 1 |
| SRP-5 | Implement upload API endpoint | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-6 | Add file validation for TXT/PDF uploads | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-7 | Add backend tests for upload endpoint | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-8 | Document upload endpoint behavior | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-10 | TXT Parsing Engine | Done | 2026-04-04 | 2026-04-07 | SRP Sprint 2 |
| SRP-16 | TXT Reader and Header Metadata Extraction | Done | 2026-04-06 | 2026-04-07 | SRP Sprint 2 |
| SRP-17 | Line Classification and Report Structure Detection | Done | 2026-04-06 | 2026-04-07 | SRP Sprint 2 |
| SRP-18 | Parse Production, Delivery, and Quantity Columns | Done | 2026-04-07 | 2026-04-07 | SRP Sprint 2 |
| SRP-19 | Parse Commercial, Credit, and Reference Columns | Done | 2026-04-07 | 2026-04-07 | SRP Sprint 2 |
| SRP-20 | Continuation Row Parsing and Parent Item Attachment | Done | 2026-04-07 | 2026-04-07 | SRP Sprint 2 |
| SRP-21 | Client and Grand Total Extraction | Done | 2026-04-07 | 2026-04-07 | SRP Sprint 2 |
| SRP-22 | Final Parser Assembly and Real Sample Tests | Done | 2026-04-07 | 2026-04-07 | SRP Sprint 2 |
| SRP-23 | Parse Core Main Row Identity and Product Columns | Done | 2026-04-07 | 2026-04-07 | SRP Sprint 2 |
| SRP-24 | Create ParsedReport model | Done | 2026-04-07 | 2026-04-08 | SRP Sprint 2 |
| SRP-25 | Create CustomerSection model | Done | 2026-04-07 | 2026-04-08 | SRP Sprint 2 |
| SRP-26 | Create ParsedItem model | Done | 2026-04-07 | 2026-04-08 | SRP Sprint 2 |
| SRP-27 | Create ContinuationRow model | Done | 2026-04-07 | 2026-04-08 | SRP Sprint 2 |
| SRP-28 | Create totals models | Done | 2026-04-07 | 2026-04-09 | SRP Sprint 2 |
| SRP-29 | Implement parser-to-model mapping service | Done | 2026-04-07 | 2026-04-09 | SRP Sprint 2 |
| SRP-30 | Add persistence tests | Done | 2026-04-07 | 2026-04-11 | SRP Sprint 2 |

### SRP-1 – Initial Project Setup

- **Status:** Done
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** No Sprint

**Description**

Set up the foundational environment for the Sales Report Processor MVP, including repository, dependencies, and basic project structure.

## Goal

Have a working development environment ready for backend implementation.

## Scope

### Included

* GitHub repository creation
* Virtual environment setup
* Core dependencies installation
* requirements.txt creation
* initial README

### Not Included

* backend features
* API endpoints
* parsing logic

## Acceptance Criteria

* Repository created
* Virtual environment configured
* Django and DRF installed
* requirements.txt exists
*  README initialized

**Comments**

_No comments_

---

### SRP-9 – Django Project and App Scaffold

- **Status:** Done
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 1

**Description**

Create the Django project structure and the `reports` app, and configure the connection to PostgreSQL. This is the technical foundation that SRP-3 and all subsequent stories depend on.

## Goal

A runnable Django project connected to PostgreSQL with the `reports` app registered and ready for feature development.

## Scope

### Included

* `django-admin startproject srp`
* `python manage.py startapp reports`
* Settings configuration (database, installed apps, media files)
* `.env.example` committed to repo

### Not Included

* Models (SRP-4)
* Any endpoints (SRP-5)
* Parsing logic

## Acceptance Criteria

* [ ] `python manage.py check` passes with no issues
* [ ] `python manage.py migrate` runs cleanly (default Django migrations only)
* [ ] `python manage.py runserver` starts without errors
* [ ] PostgreSQL connection configured via `.env`
* [ ] `reports` app registered in `INSTALLED_APPS`
* [ ] `.env.example` committed

## Technical Notes

* Use `python-decouple` for all environment variables
* `MEDIA_ROOT = BASE_DIR / 'media'`
* `media/` and `.env` must be in `.gitignore`

## Dependencies

* SRP-1 must be Done

**Comments**

- **Tailor Maciel** (2026-04-04): SRP-9 completed.

Delivered:

* Django project scaffold in backend/
* reports app created and registered
* SQLite-based MVP setup maintained
* .env.example added
* project validated with check, migrate, and runserver

This establishes the technical foundation for SRP-3 and subsequent backend stories.

---

### SRP-3 – File Upload API

- **Status:** Done
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-06
- **Sprint:** SRP Sprint 1

**Description**

Implement a backend API endpoint that allows users to upload supplier reports in TXT or PDF format.

This endpoint is the entry point of the system and initiates the report processing pipeline. It is responsible for receiving files, validating input, and storing the uploaded data for subsequent parsing and processing steps.

The implementation should be simple, reliable, and aligned with MVP scope, focusing on correctness and clarity rather than advanced features.

----

## Goal

Enable the system to accept and persist report files through an API endpoint, establishing the foundation for the parsing engine and data processing workflow.

----

## Context

In real B2B sales operations, supplier reports are typically received as:

* TXT files (structured but unformatted)
* PDF files (semi-structured or unstructured)

These files contain critical information such as:

* order numbers
* client names
* product details
* quantities
* delivery or production status

Currently, this data is often:

* manually processed
* time-consuming to extract
* difficult to integrate into systems

This API represents the *first step toward automation*, enabling the system to receive raw data and prepare it for structured processing.

----

## Scope

### Included

* Create API endpoint to upload files
* Accept TXT and PDF formats
* Validate file presence
* Validate file type (TXT/PDF only)
* Store uploaded file (local or temporary storage)
* Return success response with reference ID

----

### Not Included

* Parsing logic (handled in SRP-3)
* Data extraction
* Business validation of content
* Authentication / user context
* File deduplication or versioning

----

## Acceptance Criteria

* Endpoint exists (e.g., `/api/reports/upload/`)
* API accepts multipart file upload
* TXT and PDF files are accepted
* Invalid file types are rejected
* Missing file returns error response
* Uploaded file is stored successfully
* Response includes confirmation and file reference ID

----

## Technical Notes

* Use Django REST Framework
* Use `FileField` for storage
* Keep implementation simple (local storage acceptable)
* Ensure clear and consistent API responses
* Prepare structure for future integration with parsing service

----

## Dependencies

* SRP-1 — Initial Project Setup (completed)

**Comments**

- **Tailor Maciel** (2026-04-06): SRP-3 completed.

Delivered a fully functional backend API endpoint for uploading supplier reports (TXT/PDF), establishing the ingestion entry point of the SRP pipeline.

Implemented through the following subtasks:

* SRP-4 — UploadedReport model
• File storage using FileField (reports/)
• Upload timestamp tracking
* SRP-5 — Upload API endpoint
• POST /api/reports/upload/
• Multipart/form-data support
• File persistence and metadata response
* SRP-6 — File validation
• File presence validation
• Extension-based validation (.txt, .pdf only)
• Clear 400 error responses for invalid input
* SRP-7 — Backend tests
• Automated tests covering:
** valid TXT upload (201)
** valid PDF upload (201)
** missing file (400)
** invalid file type (400)
• Tests use SimpleUploadedFile for lightweight in-memory validation
* SRP-8 — Documentation
• Endpoint documented in README
• Request format, examples, and responses defined
• Error cases clearly described

Validation summary:

* Endpoint accepts multipart uploads correctly
* Files are persisted to backend/media/reports/
* Database stores file references and metadata
* Validation behaves as expected for all supported/unsupported cases
* Automated tests pass successfully

Scope adherence:

* Implementation remains within MVP scope
* No parsing logic, authentication, or advanced validation added
* Design prepared for future parsing integration (SRP-10)

Outcome:
A complete, reliable, and test-covered ingestion layer is now in place, forming the foundation for the parsing engine and downstream data processing workflow.

---

### SRP-4 – Create upload data model

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-3
- **Created:** 2026-04-04
- **Updated:** 2026-04-05
- **Sprint:** SRP Sprint 1

**Description**

## Purpose

Create the initial model responsible for storing uploaded report files and basic metadata.

## Scope

* Create `UploadedReport` model
* Add file field
* Add upload timestamp
* Prepare for future parsing status fields

## Deliverables

* `reports/models.py`
* migration file

## Acceptance Criteria

* Model exists
* File can be stored
* Upload timestamp is recorded
* Migration runs successfully

## Technical Notes

* App: `reports`
* Model: `UploadedReport`
* Keep model minimal for MVP
* Use `FileField(upload_to="reports/")`

## Test Expectations

* Positive case: model instance can be created with file
* Negative case: invalid migration/setup should fail visibly

**Comments**

- **Tailor Maciel** (2026-04-05): SRP-4 completed.

Delivered:

* Created UploadedReport model in reports/models.py
* Added FileField with upload_to="reports/"
* Added uploaded_at timestamp with auto_now_add=True
* Generated and applied migration successfully

Validation completed:

* Model instance created successfully in Django shell
* File persisted under media/reports/
* Timestamp recorded automatically

This establishes the data model foundation for the upload API in SRP-5.

---

### SRP-5 – Implement upload API endpoint

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-3
- **Created:** 2026-04-04
- **Updated:** 2026-04-06
- **Sprint:** SRP Sprint 1

**Description**

## Purpose

Create the DRF endpoint that receives TXT/PDF files and stores them.

## Scope

* Create API view
* Accept multipart upload
* Save file using `UploadedReport`

## Deliverables

* `reports/views.py`
* `reports/urls.py`
* project `urls.py` integration

## Acceptance Criteria

* Endpoint exists at `/api/reports/upload/`
* Multipart upload is accepted
* File is persisted
* Response returns `201 Created`

## Technical Notes

* App: `reports`
* API impact: new POST endpoint
* Use `APIView` for clarity
* Keep endpoint logic simple

## Test Expectations

* Positive case: valid TXT/PDF upload returns success
* Negative case: missing file returns `400`

**Comments**

- **Tailor Maciel** (2026-04-06): SRP-5 completed.

Delivered:

* Implemented POST /api/reports/upload/ endpoint using DRF APIView
* Configured multipart/form-data handling with MultiPartParser
* Integrated UploadedReport model for file persistence
* Wired reports.urls into project routing

Validation:

* Successful upload returns 201 with file metadata
* Missing file returns 400 with clear error message
* Files persisted under media/reports/
* Django auto-generates unique filenames for duplicates

This establishes the ingestion entry point for the SRP pipeline.

---

### SRP-6 – Add file validation for TXT/PDF uploads

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-3
- **Created:** 2026-04-04
- **Updated:** 2026-04-06
- **Sprint:** SRP Sprint 1

**Description**

## Purpose

Ensure the endpoint only accepts supported report file types.

## Scope

* Validate file presence
* Validate extension (`.txt`, `.pdf`)
* Return clear error responses

## Deliverables

* validation logic in upload endpoint

## Acceptance Criteria

* Missing file returns `400`
* Unsupported extension returns `400`
* TXT upload is accepted
* PDF upload is accepted

## Technical Notes

* Validation should remain lightweight at MVP stage
* Extension-based validation is acceptable for now
* Content inspection can be added later if needed

## Test Expectations

* Positive case: `.txt` and `.pdf` succeed
* Negative case: `.csv` or no file fails

**Comments**

- **Tailor Maciel** (2026-04-06): SRP-6 completed.

Delivered:

* Added file validation to POST /api/reports/upload/
* Restricted accepted extensions to .txt and .pdf
* Implemented clear 400 responses for unsupported file types
* Preserved missing file validation

Validation completed:

* TXT upload returns 201
* PDF upload returns 201
* CSV upload returns 400 with clear error message

Validation remains intentionally extension-based only, aligned with MVP scope.

---

### SRP-7 – Add backend tests for upload endpoint

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-3
- **Created:** 2026-04-04
- **Updated:** 2026-04-06
- **Sprint:** SRP Sprint 1

**Description**

Verify the upload endpoint works for valid and invalid requests.

## Scope

* Add API tests
* Cover success and failure cases

## Deliverables

* `reports/tests/test_upload_api.py`

## Acceptance Criteria

* Valid TXT upload returns `201`
* Valid PDF upload returns `201`
* Missing file returns `400`
* Invalid file type returns `400`

## Technical Notes

* Use DRF test client
* Keep fixtures minimal
* Prefer small in-memory test files

## Test Expectations

* Positive case: upload success
* Negative case: validation failure

**Comments**

- **Tailor Maciel** (2026-04-06): SRP-7 completed.

Delivered:

* Added backend API tests for POST /api/reports/upload/
* Covered valid TXT upload
* Covered valid PDF upload
* Covered missing file request
* Covered invalid file type rejection

Validation completed:

* 4 tests discovered
* 4 tests passed successfully

This formalizes the upload endpoint behavior already validated manually in SRP-5 and SRP-6.

---

### SRP-8 – Document upload endpoint behavior

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-3
- **Created:** 2026-04-04
- **Updated:** 2026-04-06
- **Sprint:** SRP Sprint 1

**Description**

Document the endpoint purpose, request format, and expected responses.

## Scope

* Update README or docs
* Add endpoint path
* Add sample request/response

## Deliverables

* `README.md` or `docs/api_upload.md`

## Acceptance Criteria

* Endpoint is documented
* Request format is shown
* Success response example is shown
* Error response example is shown

## Technical Notes

* Keep documentation minimal and practical
* Focus on developer usability

## Test Expectations

* Positive case: another developer can use endpoint from docs
* Negative case: none required

**Comments**

- **Tailor Maciel** (2026-04-06): SRP-8 completed.

Delivered:

* Documented POST /api/reports/upload/ endpoint in README
* Defined request format (multipart/form-data with "file" field)
* Added working curl example for file upload
* Provided success response example (201 Created with metadata)
* Documented error responses:
** Missing file (400)
** Unsupported file type (400)
* Listed supported file types (.txt, .pdf)
* Documented file storage behavior (media/reports/) and DB reference model

Validation:

* Documentation aligns with actual endpoint behavior implemented in SRP-5 and SRP-6
* Examples verified via curl and Postman

This completes the upload ingestion flow documentation for the SRP MVP and makes the endpoint usable by other developers without additional guidance.

---

### SRP-10 – TXT Parsing Engine

- **Status:** Done
- **Type:** Story
- **Parent:** SRP-2
- **Created:** 2026-04-04
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Implement a TXT parsing engine for the supplier report format currently used in SRP: *“Relação dos Pedidos em Carteira”*.

The parser must process uploaded TXT files generated in this fixed-width, column-based format and convert them into structured Python data preserving the complete report structure and all relevant fields.

⚠️ *Scope clarification (important):*

This implementation must support:

{quote}*Full field coverage for the current carteira report format only.*{quote}

It must *NOT attempt to support generic TXT formats or other supplier layouts* at this stage.

The parser must extract:

* report metadata from header lines
* customer sections
* main order rows
* continuation rows
* client totals
* report grand totals

Unlike a generic MVP parser, this story must cover the *full set of report columns* present in the current real sample, because those fields contain operational, commercial, logistics, and credit information that cannot be safely ignored. The implementation must remain readable, testable, and aligned with the current SRP scope.

## Goal

Convert the uploaded carteira TXT report into structured Python data with complete field coverage, preserving hierarchy and business meaning, ready for persistence in SRP-11.

## Scope

### Included

* Full column extraction for the current carteira report format (all fields listed in this story)
* Read TXT file content from uploaded report storage
* Decode text safely, handling imperfect encoding when necessary
* Normalize lines and remove report noise such as repeated page headers and separators
* Parse report header metadata, including:
** report title
** generated date
** generated time
** page number when present
* Detect customer blocks using lines such as `Rep: ... Cliente: ...`
* Parse all columns from main detail rows
* Parse continuation rows and attach them to the correct parent row
* Parse per-client totals
* Parse report grand totals
* Preserve raw source lines for traceability
* Return a structured parse result ready for SRP-11 model mapping
* Add parser tests based on the real uploaded sample

### Not Included

* PDF parsing
* OCR
* parsing other supplier TXT formats not represented by the current carteira sample
* Generic parsing engine for unknown file structures
* database persistence
* retrieval API
* dashboard/UI work
* analytics or business recommendation logic

## Full Field Coverage Required

The parser must support the following fields from the report structure:

### Report metadata

* report_title
* generated_date
* generated_time
* folha / page number when available

### Customer block metadata

* representative
* customer_name

### Main row columns

* est
* pedido
* seq
* descricao
* espess
* larg
* compr
* ord_prod
* sit_ordem
* dt_entr
* aa
* qt_ped
* qt_pc
* qt_prod
* qt_fatur
* sdo_estoq
* sit
* pre_liq
* pf
* vlr_peca
* pag
* transp
* cr_pro
* cr_fat
* o_compra
* item_cli
* mnf

### Continuation row fields

* additional production/order references tied to the parent row
* continuation status values
* continuation raw line

### Totals

* client total quantities
* client total in currency
* grand total quantities
* grand total in currency

## Acceptance Criteria

* Parser service exists inside the `reports` app
* TXT file can be read and normalized successfully
* Report header metadata is extracted correctly, including date and time from header lines
* Customer sections are detected correctly
* Main detail rows are parsed with full field coverage
* Continuation rows are attached to the correct parent row
* Client totals are extracted correctly
* Grand totals are extracted correctly
* Output preserves hierarchy: report → customers → items → continuations
* Raw source lines are preserved for traceability
* Parser handles empty files, malformed lines, and encoding issues gracefully
* Tests validate parsing against the real carteira sample
* Implementation remains within SRP-10 scope and does not include persistence or API exposure

## Technical Notes

The real uploaded sample is not a simple key-value TXT; it is a fixed-width operational report with repeated customer sections, continuation rows, client totals, and grand totals. The parser design must reflect that actual structure. The sample clearly shows the report title, timestamp, `Rep` and `Cliente` sections, detail rows, `TOT CLIENTE`, `TOTAL CLIENTE EM R$`, `TOTAL GERAL`, and `TOTAL EM R$`.

The current SRP backlog places SRP-10 as the next story after upload completion, with SRP-11 handling parsed data models after this. That makes SRP-10 the right place to define and validate full extraction logic, while leaving persistence to the next story. 

## Dependencies

* SRP-3 – File Upload API ✅ Done

## Suggested Story Points

* 13

### SRP-10 – Subtask Execution Plan & Dependencies

To ensure a structured and incremental implementation of the TXT parsing engine, the subtasks will be executed in the following order:

*Execution Order*

# SRP-16 — TXT Reader and Header Metadata Extraction
# SRP-17 — Line Classification and Report Structure Detection
# SRP-23 — Parse Core Main Row Identity and Product Columns
# SRP-18 — Parse Production, Delivery, and Quantity Columns
# SRP-19 — Parse Commercial, Credit, and Reference Columns
# SRP-20 — Continuation Row Parsing and Parent Item Attachment
# SRP-21 — Client and Grand Total Extraction
# SRP-22 — Final Parser Assembly and Real Sample Tests

----

*Dependency Flow*

* SRP-16 → SRP-17
* SRP-17 → SRP-23
* SRP-23 → SRP-18
* SRP-18 → SRP-19
* SRP-19 → SRP-20
* SRP-17 → SRP-21
* SRP-20 + SRP-21 → SRP-22

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-10 completed.

Delivered:

* Fully implemented TXT Parsing Engine for carteira report format
* Achieved full field coverage for the current report structure

Subtasks completed:

* SRP-16: TXT reader and metadata extraction
* SRP-17: Line classification and structure detection
* SRP-23: Main row identity and product columns
* SRP-18: Operational and quantity columns
* SRP-19: Commercial, credit, and reference columns
* SRP-20: Continuation row parsing and attachment
* SRP-21: Client and grand totals extraction
* SRP-22: Final parser assembly and structured output

Key Capabilities:

* Transforms raw TXT report into structured business dataset
* Supports hierarchical structure (main rows + continuation rows)
* Extracts all relevant commercial, operational, and financial fields
* Handles variable-width fields and mixed formatting robustly
* Preserves traceability through raw line retention

Validation:

* Full test suite implemented and passing
* Real carteira sample used for validation across all stages

Notes:

* Parsing is scoped to the current carteira report format (MVP scope)
* Designed with layered parsing strategy:
fixed-width → token-based → tail parsing → hierarchical assembly

Outcome:

* Parsing engine is complete and ready for integration with API and dashboard layers

TXT parsing engine (SRP-10) completed.

The system can now ingest supplier reports (TXT), extract structured data, and produce a business-ready dataset.

Next phase:

* SRP-12 (Processed Data Retrieval API)
* SRP-13 (Basic Dashboard View)

---

### SRP-16 – TXT Reader and Header Metadata Extraction

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-06
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Create the foundation for reading the report safely and extracting report-level metadata from header lines.

## Scope

* Read TXT from disk
* Handle decoding safely
* Normalize line endings and spacing
* Extract:
** report title
** generated date
** generated time
** folha / page number when present

## Deliverables

* `reports/services/txt_parser.py`
* Reader and header parsing functions

## Acceptance Criteria

* File is read without crashing
* Header metadata is extracted correctly from the real sample
* Repeated page headers can be recognized and ignored during detail parsing

## Technical Notes

* Files: `reports/services/txt_parser.py`
* API impact: none
* Validation notes: preserve original raw text for debugging

## Dependencies

* SRP-3 must be Done

## Suggested Story Points

* 2

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-16 completed.

Delivered:

* Implemented initial TXT reader service in reports/services/txt_parser.py
* Added safe file reading with UTF-8 and latin-1 fallback
* Normalized line endings and cleaned line content for downstream parsing
* Preserved raw_text and normalized lines for later parser stages
* Extracted generated_date and generated_time from the real carteira TXT sample
* Added automated tests in reports/tests/test_txt_parser.py

Validation:

* python manage.py test reports.tests.test_txt_parser
* 3 tests passed successfully

Notes:

* Test path uses the actual uploaded report location:
backend/media/reports/carteira_06_04_26.txt

This completes the reader/header foundation needed before SRP-17 line classification.

---

### SRP-17 – Line Classification and Report Structure Detection

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-06
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Classify lines and identify the structural boundaries of the report.

## Scope

* Classify:
** report headers
** customer headers
** table headers
** separator lines
** main detail rows
** continuation rows
** client totals
** grand totals
** ignorable lines

## Deliverables

* Line classification helpers
* Structural parsing state machine or equivalent logic

## Acceptance Criteria

* Customer blocks are recognized correctly
* Main rows and continuation rows are distinguished correctly
* Totals lines are distinguished correctly

## Technical Notes

* Files: `reports/services/txt_parser.py`
* API impact: none
* Validation notes: unknown lines must not crash parsing

## Dependencies

* SRP-10 reader/header subtask

## Suggested Story Points

* 2

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-17 completed.

Delivered:

* Implemented line classification system for carteira TXT reports
* Added classification for:


 customer headers, separators, table headers,
 main rows, continuation rows, totals, and ignorable lines

* Implemented classify_line and classify_report_lines helpers
* Implemented customer block detection with representative and customer_name extraction
* Preserved raw lines and structure for downstream parsing stages

Validation:

* python manage.py test reports.tests.test_txt_parser
* 6 tests passed successfully

Notes:

* Implementation strictly focused on structure detection (no field parsing)
* Output prepares the parser for SRP-23 (main row identity parsing)

SRP-17 is complete and ready for next step in parsing pipeline.

---

### SRP-18 – Parse Production, Delivery, and Quantity Columns

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-07
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Extract the operational fields that track production, delivery, and quantities.

## Scope

* Parse:
** ord_prod
** sit_ordem
** dt_entr
** aa
** qt_ped
** qt_pc
** qt_prod
** qt_fatur
** sdo_estoq
** sit

## Deliverables

* Operational and quantity parsing logic for main rows

## Acceptance Criteria

* Dates are extracted correctly
* Quantity columns map correctly

* Status values are extracted without corrupting adjacent columns

## Technical Notes

* Files: `reports/services/txt_parser.py`
* API impact: none
* Validation notes: numeric strings may remain strings in SRP-10; normalization can be finalized in SRP-11

## Dependencies

* SRP-10 core main-row parsing subtask

## Suggested Story Points

* 2

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-18 completed.

Delivered:

* Implemented parsing for operational and quantity columns from main detail rows
* Added extraction of:


 ord_prod, sit_ordem, dt_entr, aa,
 qt_ped, qt_pc, qt_prod, qt_fatur, sdo_estoq, sit

* Combined SRP-23 identity/product parsing with SRP-18 operational parsing
* Added automated tests using real carteira sample rows

Validation:

* python manage.py test reports.tests.test_txt_parser
* 10 tests passed successfully

Notes:

* Identity/product fields remain fixed-width based
* Operational fields are parsed from the remainder after `compr` using


 tokenization anchored by the date column

* This is more robust for variable-width quantity values and multiword status fields

SRP-18 is complete and ready for SRP-19.

---

### SRP-19 – Parse Commercial, Credit, and Reference Columns

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-07
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Extract the commercial and credit-related fields that are important for downstream business use.

## Scope

* Parse:
** pre_liq
** pf
** vlr_peca
** pag
** transp
** cr_pro
** cr_fat
** o_compra
** item_cli
** mnf

## Deliverables

* Fixed-width parsing logic for commercial and reference columns

## Acceptance Criteria

* Known sample rows return correct values for these columns when present
* Blank fields are handled safely
* No adjacent-column leakage occurs in parsed output

## Technical Notes

* Files: `reports/services/txt_parser.py`
* API impact: none
* Validation notes: `mnf` is optional and may be blank for many rows

## Dependencies

* SRP-10 operational/quantity parsing subtask

## Suggested Story Points

* 2

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-19 completed.

Delivered:

* Implemented parsing for commercial, credit, and reference columns
* Added extraction of:


 pre_liq, pf, vlr_peca, pag, transp,
 cr_pro, cr_fat, o_compra, item_cli, mnf

* Implemented tail-based parsing strategy anchored by date and price tokens
* Added support for optional PF column
* Combined SRP-23, SRP-18, and SRP-19 into a full row parser
* Added automated tests using real carteira sample

Validation:

* python manage.py test reports.tests.test_txt_parser
* 11 tests passed successfully

Notes:

* Parser preserves original decoded text (including encoding artifacts)
* Strategy ensures robustness for variable-width fields and multiword values

SRP-19 is complete and row-level parsing is now fully implemented.

---

### SRP-20 – Continuation Row Parsing and Parent Item Attachment

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-07
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Parse continuation rows and attach them to the correct main item.

## Scope

* Detect continuation rows
* Parse continuation values such as:
** additional production/order references
** continuation status
** raw continuation line
* Attach continuation rows to the most recent valid parent item

## Deliverables

* Continuation parsing functions
* Parent-child row attachment logic

## Acceptance Criteria

* Continuation rows are linked to the correct item
* Multiple continuation rows can be stored under one item
* Orphan continuation rows are handled safely

## Technical Notes

* Files: `reports/services/txt_parser.py`
* API impact: none
* Validation notes: retain continuation raw lines even when partially parsed

## Dependencies

* SRP-10 main-row parsing subtasks

## Suggested Story Points

* 1

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-20 completed.

Delivered:

* Implemented parsing for continuation rows
* Added extraction of:


 ord_prod, sit_ordem, qt_prod, sit

* Implemented attachment of continuation rows to the most recent valid parent main row
* Preserved raw continuation lines for traceability
* Added automated tests using the real carteira sample

Validation:

* python manage.py test reports.tests.test_txt_parser
* 12 tests passed successfully

Notes:

* Continuation rows use a reduced operational structure compared with main rows
* Parsing uses token-based extraction to handle variable spacing safely
* Parser output now preserves parent-child hierarchy between main rows and continuation rows

SRP-20 is complete and ready for SRP-21.

---

### SRP-21 – Client and Grand Total Extraction

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-07
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Extract totals at both customer and whole-report levels.

## Scope

* Parse:
** `TOT CLIENTE`
** `TOTAL CLIENTE EM R$`
** `TOTAL GERAL`
** `TOTAL EM R$`

## Deliverables

* Totals parsing logic
* Assignment of totals to correct customer block or report summary

## Acceptance Criteria

* Client totals are assigned to the correct customer
* Grand totals are extracted correctly
* Currency total lines are stored separately from quantity total lines when appropriate

## Technical Notes

* Files: `reports/services/txt_parser.py`
* API impact: none
* Validation notes: totals should remain traceable to their original raw lines

## Dependencies

* SRP-10 line classification subtask

## Suggested Story Points

* 1

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-21 completed.

Delivered:

* Implemented extraction for client and grand total lines
* Added support for:


 TOT CLIENTE
 TOTAL CLIENTE EM R$
 TOTAL GERAL
 TOTAL EM R$

* Added numeric extraction helper for totals parsing
* Added collection of totals across the report
* Added automated tests using the real carteira sample

Validation:

* python manage.py test reports.tests.test_txt_parser
* 13 tests passed successfully

Notes:

* Totals parsing builds directly on SRP-17 line classification
* Output now includes both quantity totals and currency totals
* Parser is now ready for final end-to-end assembly in SRP-22

SRP-21 is complete and ready for SRP-22.

---

### SRP-22 – Final Parser Assembly and Real Sample Tests

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-07
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Assemble the complete parser pipeline and validate it with the real uploaded sample.

## Scope

* Build end-to-end `parse_txt_report(...)`
* Return final structured dictionary
* Add tests for:
** header metadata
** customer detection
** full row extraction
** continuation attachment
** totals extraction
** empty/malformed file handling

## Deliverables

* `reports/services/txt_parser.py`
* `reports/tests/test_txt_parser.py`

## Acceptance Criteria

* Full report parses end-to-end
* Tests pass against the real sample structure
* Output is ready to map into SRP-11 models

## Technical Notes

* Files: `reports/services/txt_parser.py`, `reports/tests/test_txt_parser.py`
* API impact: none
* Validation notes: test at least one known row with many populated columns

## Dependencies

* All prior SRP-10 subtasks

## Suggested Story Points

* 1

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-22 completed.

Delivered:

* Implemented full parser assembly combining all previous stages:
SRP-16 (reader), SRP-17 (structure),
SRP-23/SRP-18/SRP-19 (row parsing),
SRP-20 (continuation rows),
SRP-21 (totals)
* Built final structured output including:
metadata, customer blocks, items with continuations,
client totals, and grand totals
* Implemented assemble_report as the entry point for full parsing
* Added end-to-end test validating full report structure

Validation:

* python manage.py test reports.tests.test_txt_parser
* All tests passed successfully

Notes:

* Parser now transforms raw TXT into structured business-ready data
* Output is suitable for API exposure, analytics, and dashboard consumption
* Marks completion of the SRP parsing engine MVP

SRP-22 is complete.

---

### SRP-23 – Parse Core Main Row Identity and Product Columns

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-10
- **Created:** 2026-04-07
- **Updated:** 2026-04-07
- **Sprint:** SRP Sprint 2

**Description**

Extract the main identifying and product-related fields from primary detail rows.

## Scope

* Parse:
** est
** pedido
** seq
** descricao
** espess
** larg
** compr

## Deliverables

* Main-row fixed-width parsing for identity and material columns

## Acceptance Criteria

* Known sample rows return correct values for the listed fields
* Missing or shifted values do not break parsing flow
* Raw line is preserved with each parsed item

## Technical Notes

* Files: `reports/services/txt_parser.py`
* API impact: none
* Validation notes: preserve exact source line for every parsed row

## Dependencies

* SRP-10 line classification subtask

## Suggested Story Points

* 2

**Comments**

- **Tailor Maciel** (2026-04-07): SRP-23 completed.

Delivered:

* Implemented parsing for main-row identity and product columns
* Added extraction of:


 est, pedido, seq, descricao, espess, larg, compr

* Preserved raw_line for every parsed main detail row
* Added helper to parse all lines classified as main_detail
* Added automated tests using real carteira sample rows

Validation:

* python manage.py test reports.tests.test_txt_parser
* 9 tests passed successfully

Notes:

* Parsing uses fixed-width slicing based on the real carteira layout
* This avoids leakage when numeric values appear inside descricao
* Output prepares the parser for SRP-18 operational and quantity column extraction

SRP-23 is complete and ready for the next parsing stage.

---

### SRP-24 – Create ParsedReport model

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-11
- **Created:** 2026-04-07
- **Updated:** 2026-04-08
- **Sprint:** SRP Sprint 2

**Description**

Create the top-level model representing one parsed TXT report.

*Scope*

* Link parsed report to `UploadedReport`
* Store report-level metadata:
** `generated_date`
** `generated_time`

*Deliverables*

* `ParsedReport` model
* migration

*Acceptance Criteria*

* ParsedReport can be created from an existing UploadedReport
* Generated date/time can be stored
* Migration runs successfully

**Comments**

- **Tailor Maciel** (2026-04-08): SRP-24 completed.

Delivered:

* Implemented ParsedReport model
* Linked ParsedReport to UploadedReport via ForeignKey
* Added metadata fields: generated_date and generated_time
* Added created_at timestamp
* Created and applied migrations
* Added basic model test

Validation:

* python manage.py test
* All tests passed successfully

Notes:

* ParsedReport serves as the root entity for structured parsed data
* Design keeps date/time as strings to match parser output (MVP scope)

SRP-24 is complete and ready for SRP-25.

---

### SRP-25 – Create CustomerSection model

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-11
- **Created:** 2026-04-07
- **Updated:** 2026-04-08
- **Sprint:** SRP Sprint 2

**Description**

Persist each customer block detected in the parsed report.

*Scope*

* FK to `ParsedReport`
* Store:
** `representative`
** `customer_name`

*Deliverables*

* `CustomerSection` model
* migration

*Acceptance Criteria*

* Multiple customer sections can be linked to one ParsedReport
* Representative and customer name are stored correctly
* Migration runs successfully

**Comments**

- **Tailor Maciel** (2026-04-08): SRP-25 completed.

Delivered:

* Implemented CustomerSection model
* Linked CustomerSection to ParsedReport via ForeignKey
* Added fields: representative and customer_name
* Added created_at timestamp
* Created and applied migrations
* Added model test validating relationship

Validation:

* python manage.py test
* All tests passed successfully

Notes:

* Establishes first hierarchical layer of parsed data (report → customers)
* Prepares structure for ParsedItem (SRP-26)

SRP-25 is complete.

---

### SRP-26 – Create ParsedItem model

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-11
- **Created:** 2026-04-07
- **Updated:** 2026-04-08
- **Sprint:** SRP Sprint 2

**Description**

Store full parsed main-detail rows for each customer section.

*Scope*

* FK to `CustomerSection`
* Store all main-row fields from SRP-23, SRP-18, and SRP-19

*Included Fields*

* identity/product:
** `est`
** `pedido`
** `seq`
** `descricao`
** `espess`
** `larg`
** `compr`
* operational/quantity:
** `ord_prod`
** `sit_ordem`
** `dt_entr`
** `aa`
** `qt_ped`
** `qt_pc`
** `qt_prod`
** `qt_fatur`
** `sdo_estoq`
** `sit`
* commercial/reference:
** `pre_liq`
** `pf`
** `vlr_peca`
** `pag`
** `transp`
** `cr_pro`
** `cr_fat`
** `o_compra`
** `item_cli`
** `mnf`
* traceability:
** `raw_line`

*Deliverables*

* `ParsedItem` model
* migration

*Acceptance Criteria*

* Parsed items can be stored under the correct customer section
* All main-row fields are represented
* Raw line is preserved
* Migration runs successfully

**Comments**

- **Tailor Maciel** (2026-04-08): SRP-26 completed.

Delivered:

* Implemented ParsedItem model
* Linked ParsedItem to CustomerSection via ForeignKey
* Added full field coverage for:
** identity and product data
** operational fields
** quantities
** commercial and credit fields
* Added raw_line field for traceability
* Added created_at timestamp
* Created and applied migrations
* Added model test

Validation:

* python manage.py test
* All tests passed successfully

Notes:

* Model preserves full structure of parsed TXT rows
* All fields stored as strings to match parser output (MVP scope)
* Represents the core business data layer of the system

SRP-26 is complete.

---

### SRP-27 – Create ContinuationRow model

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-11
- **Created:** 2026-04-07
- **Updated:** 2026-04-08
- **Sprint:** SRP Sprint 2

**Description**

Store continuation rows linked to their parent parsed item.

*Scope*

* FK to `ParsedItem`
* Store:
** `ord_prod`
** `sit_ordem`
** `qt_prod`
** `sit`
** `raw_line`

*Deliverables*

* `ContinuationRow` model
* migration

*Acceptance Criteria*

* Multiple continuation rows can be linked to one ParsedItem
* Reduced continuation structure is preserved
* Raw continuation line is stored
* Migration runs successfully

**Comments**

- **Tailor Maciel** (2026-04-08): SRP-27 completed.

Delivered:

* Implemented ContinuationRow model
* Linked ContinuationRow to ParsedItem via ForeignKey
* Added fields: ord_prod, sit_ordem, qt_prod, sit
* Added raw_line field for traceability
* Added created_at timestamp
* Created and applied migrations
* Added model test validating persistence and relationships

Validation:

* python manage.py test
* All tests passed successfully

Notes:

* Completes hierarchical structure for parsed items
* Supports multi-line item representation from TXT reports

SRP-27 is complete.

---

### SRP-28 – Create totals models

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-11
- **Created:** 2026-04-07
- **Updated:** 2026-04-09
- **Sprint:** SRP Sprint 2

**Description**

Persist totals extracted in SRP-21.

*Scope*
Choose a simple MVP structure:

* `CustomerTotal`
** FK to `CustomerSection`
** quantity totals
** currency total
* `ReportGrandTotal`
** OneToOne or FK to `ParsedReport`
** quantity totals
** currency total

*Fields*

* quantity totals:
** `total_ped`
** `total_pc`
** `total_prod`
** `total_fatur`
** `total_sdo`
* currency:
** `total_valor`

*Deliverables*

* totals model(s)
* migration

*Acceptance Criteria*

* Customer-level totals can be stored correctly
* Report-level totals can be stored correctly
* Quantity totals and currency totals are both preserved
* Migration runs successfully

**Comments**

- **Tailor Maciel** (2026-04-09): *SRP-28 Completed — Totals Parsing and Models*

Implemented full support for extracting and structuring totals from TXT reports, aligned with real report format.

*Key Deliverables:*

* Parsed client and grand totals (quantities and currency values)
* Standardized field naming (`total_in_prod`) across parser and models
* Implemented `CustomerTotal` and `ReportTotal` models with proper relationships
* Ensured totals from multiple lines are unified into single model records
* Strengthened tests with exact value assertions for reliability
* Resolved migration inconsistencies and validated schema alignment

*Outcome:*
Totals data is now accurately extracted and ready for persistence in the next stage.

*Next Step:*
Proceed to *SRP-29 — Persistence Layer*, connecting parsing output to database storage.

----

---

### SRP-29 – Implement parser-to-model mapping service

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-11
- **Created:** 2026-04-07
- **Updated:** 2026-04-09
- **Sprint:** SRP Sprint 2

**Description**

Create the service layer that takes SRP-22 structured output and saves it into the database.

*Scope*

* Map `assemble_report(...)` output into:
** ParsedReport
** CustomerSection
** ParsedItem
** ContinuationRow
** totals models
* Keep implementation simple and deterministic

*Deliverables*

* persistence service in `reports/services/`
* minimal save function, for example:
** `save_parsed_report(uploaded_report)`

*Acceptance Criteria*

* A parsed TXT report can be persisted end-to-end
* Relationships are created correctly
* Continuations attach to the correct ParsedItem
* Totals are stored in the correct scope

**Comments**

- **Tailor Maciel** (2026-04-09): SRP-29 Completed — Report Persistence Pipeline

Implemented the persistence layer connecting parsed TXT data to database models.

Key Deliverables:

* Created persist_report service to orchestrate full persistence workflow
* Persisted ParsedReport, CustomerSection, ParsedItem, and ContinuationRow
* Implemented CustomerTotal and ReportTotal with correct relationships
* Ensured OneToOne integrity by always creating ReportTotal
* Aligned parser output with model structure
* Added tests validating end-to-end persistence

Outcome:
System now supports full pipeline from uploaded file to structured database records.

Next Step:
Proceed to SRP-12 — Processed Data Retrieval API

---

### SRP-30 – Add persistence tests

- **Status:** Done
- **Type:** Subtask
- **Parent:** SRP-11
- **Created:** 2026-04-07
- **Updated:** 2026-04-11
- **Sprint:** SRP Sprint 2

**Description**

Validate that parsed output is saved correctly into the database.

*Scope*

* Test:
** ParsedReport creation
** CustomerSection creation
** ParsedItem persistence
** ContinuationRow persistence
** totals persistence
* Validate relationships and counts using the real sample structure

*Deliverables*

* model/service tests

*Acceptance Criteria*

* Tests confirm full persistence flow works
* Relationships are correct
* No data is silently lost during mapping
* Test suite passes

**Comments**

- **Tailor Maciel** (2026-04-11): Completed SRP-30 by adding backend persistence tests for the parsed report flow.

Delivered:

* tests for ParsedReport creation
* tests for CustomerSection persistence
* tests for ParsedItem persistence
* tests for ContinuationRow persistence
* tests for CustomerTotal and ReportTotal persistence
* relationship validation across persisted entities
* persistence validation using the real sample TXT structure
* persistence validation using mocked assembled parser output

Implementation note:
During test implementation, a small set of parser and payload-alignment corrections was required so the assembled report structure matched the persistence contract used by the service layer. These were corrective changes needed to make persistence verification accurate and runnable. They do not add new MVP features and were made only to support correct SRP-30 test coverage.

Result:

* full persistence flow is now covered by tests
* relationships and mapped totals are verified
* data loss during persistence mapping is checked
* acceptance criteria for SRP-30 are satisfied

---

