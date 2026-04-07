# Jira Backlog for Project SRP
_Exported: 2026-04-06 21:09:55_

**Total Issues:** 15

## Summary

- **To Do:** 7 issues
- **In Progress:** 2 issues
- **Done:** 6 issues

---

## To Do (7 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-15 | Documentation and Demo Readiness | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 4 |
| SRP-14 | Error Handling and Validation | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 4 |
| SRP-13 | Basic Dashboard View | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 3 |
| SRP-12 | Processed Data Retrieval API | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 3 |
| SRP-11 | Parsed Data Models | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 2 |
| SRP-10 | TXT Parsing Engine | To Do | 2026-04-04 | 2026-04-04 | SRP Sprint 2 |
| SRP-2 | Sales Report Processor MVP | To Do | 2026-04-04 | 2026-04-04 | No Sprint |

### SRP-15 – Documentation and Demo Readiness

- **Status:** To Do
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 4

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-14 – Error Handling and Validation

- **Status:** To Do
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 4

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-13 – Basic Dashboard View

- **Status:** To Do
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 3

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-12 – Processed Data Retrieval API

- **Status:** To Do
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 3

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-11 – Parsed Data Models

- **Status:** To Do
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 2

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-10 – TXT Parsing Engine

- **Status:** To Do
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Sprint:** SRP Sprint 2

**Description**

_No content_

**Comments**

_No comments_

---

### SRP-2 – Sales Report Processor MVP

- **Status:** To Do
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

## In Progress (2 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-8 | Document upload endpoint behavior | In Progress | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-3 | File Upload API | In Progress | 2026-04-04 | 2026-04-05 | SRP Sprint 1 |

### SRP-8 – Document upload endpoint behavior

- **Status:** In Progress
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

_No comments_

---

### SRP-3 – File Upload API

- **Status:** In Progress
- **Created:** 2026-04-04
- **Updated:** 2026-04-05
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

_No comments_

---

## Done (6 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-9 | Django Project and App Scaffold | Done | 2026-04-04 | 2026-04-04 | SRP Sprint 1 |
| SRP-7 | Add backend tests for upload endpoint | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-6 | Add file validation for TXT/PDF uploads | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-5 | Implement upload API endpoint | Done | 2026-04-04 | 2026-04-06 | SRP Sprint 1 |
| SRP-4 | Create upload data model | Done | 2026-04-04 | 2026-04-05 | SRP Sprint 1 |
| SRP-1 | Initial Project Setup | Done | 2026-04-04 | 2026-04-04 | No Sprint |

### SRP-9 – Django Project and App Scaffold

- **Status:** Done
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

### SRP-7 – Add backend tests for upload endpoint

- **Status:** Done
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

### SRP-6 – Add file validation for TXT/PDF uploads

- **Status:** Done
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

### SRP-5 – Implement upload API endpoint

- **Status:** Done
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

### SRP-4 – Create upload data model

- **Status:** Done
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

### SRP-1 – Initial Project Setup

- **Status:** Done
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

