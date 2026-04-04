# Jira Backlog for Project SRP
_Exported: 2026-04-04 16:57:53_

**Total Issues:** 2

## Summary

- **To Do:** 1 issues
- **In Progress:** 0 issues
- **Done:** 1 issues

---

## To Do (1 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-2 | Sales Report Processor MVP | To Do | 2026-04-04 | 2026-04-04 | No Sprint |

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

## Done (1 issues)

| Key | Summary | Status | Created | Updated | Sprint |
|-----|---------|--------|---------|---------|--------|
| SRP-1 | Initial Project Setup | Done | 2026-04-04 | 2026-04-04 | No Sprint |

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

