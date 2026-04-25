<!--
Purpose: Public architecture and design overview for the SRP MVP.
Date: 2026-04-24
Author: Codex
Domain: Systems / SRP
-->

# SRP Architecture Overview

## Purpose

This document explains how the Sales Report Processor MVP is structured and how
its main pieces fit together.

## Business Context

The system targets a real operational problem in industrial B2B sales:
supplier reports arrive as raw text-heavy files, but sales follow-up requires a
clear view of delays, balances, client concentration, and next actions.

SRP converts that raw report layer into:

- structured persisted data
- retrieval endpoints
- a daily operational dashboard

## Core Flow

The MVP follows this pipeline:

1. upload raw supplier report
2. validate file type and presence
3. parse TXT report content into structured fields
4. persist structured report data
5. expose processed data through the API
6. render the latest processed report in the dashboard

## Main Layers

### Upload Layer

- accepts TXT and PDF files
- stores uploaded files under Django media handling
- returns clear success and validation-error responses

Relevant endpoint:

- `POST /api/reports/upload/`

### Parsing Layer

- reads TXT report content
- extracts header metadata, customer sections, items, continuation rows, and
  totals
- keeps parsing logic out of views and templates

### Persistence Layer

- converts parsed output into `ParsedReport` plus related models
- enforces a minimum processing contract before writes begin
- uses atomic persistence so failed writes do not leave partial structured data

### Retrieval Layer

- exposes list and detail views for processed reports
- supports lightweight summary access and full nested detail access

Relevant endpoints:

- `GET /api/reports/`
- `GET /api/reports/{id}/`

### Dashboard Layer

- renders the latest persisted parsed report
- converts structured data into a story-driven operational briefing
- keeps business logic in the dashboard service instead of templates

Relevant endpoint:

- `GET /dashboard/`

## Dashboard Design Intent

The dashboard is meant to answer:

- what needs attention now
- where operational pressure is concentrated
- which clients deserve immediate follow-up
- what context the sales representative needs before acting

Current reading flow:

- `Indicadores Principais`
- `Visao Operacional`
- `Excecoes Operacionais`
- `Fila de Prioridades`
- `Carteira em Foco`
- `Clientes em Evidencia`
- `Cliente 360`
- `Timeline de Entregas`

## Engineering Decisions

The MVP deliberately favors:

- Django templates instead of a SPA
- service-layer business logic instead of logic-heavy views/templates
- explicit validation over silent failure
- tests close to the changed behavior
- simple local execution over deployment complexity

## Current Limits

The project intentionally does not include:

- advanced PDF parsing
- authentication and permissions
- background workers or async processing
- deployment packaging
- advanced frontend architecture

## What This Demonstrates

SRP is a showcase of:

- business-oriented backend design
- parsing and persistence work on non-trivial text inputs
- operational dashboard design tied to real workflows
- iterative, test-backed MVP delivery
