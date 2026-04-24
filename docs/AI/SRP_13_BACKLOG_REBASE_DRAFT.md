# SRP_13_BACKLOG_REBASE_DRAFT.md
## Purpose
Provide Jira-ready replacement wording for SRP-13 and its subtasks so backlog
tracking can be re-baselined to the implemented dashboard rather than the older
literal contract.
## Date
2026-04-24
## Author
Codex
## Domain
Systems / Sales Report Processor (SRP)

# SRP-13 Backlog Rebase Draft

## Recommended Status Changes

- `SRP-35` -> mark as locally satisfied
- `SRP-36` -> mark as locally satisfied
- `SRP-37` -> mark as locally satisfied
- `SRP-38` -> mark as locally satisfied
- `SRP-13` -> move from `In Progress` toward formal closure after backlog text
  is updated

## Jira Story: SRP-13 – Basic Dashboard View

## Description

Implement the SRP dashboard as a server-rendered operational page focused on
the sales representative's daily reading flow.

The dashboard uses the latest persisted parsed report to surface:

- top operational KPIs
- concentration of pressure
- a priority queue for immediate follow-up
- a client-priority portfolio view
- a focused client drilldown
- supporting timeline and exception detail

The implemented page is intentionally story-driven rather than a collection of
disconnected widgets. The expected reading flow is:

- `Indicadores Principais`
- `Visao Operacional`
- `Excecoes Operacionais`
- `Fila de Prioridades`
- `Carteira em Foco`
- `Clientes em Evidencia`
- `Cliente 360`
- `Timeline de Entregas`

The page must remain implementation-simple:

- Django template based
- read-only
- no React
- no background jobs
- no automation actions
- no parser expansion

## Goal

Deliver one useful dashboard page that turns persisted report data into
practical daily sales priorities through a queue-centered and client-focused
operational flow.

## Scope

### Included

- Add a human-facing dashboard route at `GET /dashboard/`
- Use the latest persisted `ParsedReport` as the dashboard source
- Show a KPI strip with report totals and operational orientation
- Show deterministic priority logic through a queue-centered action surface
- Show a client portfolio table ordered by business priority
- Show downstream drilldown context for the first-ranked focused client
- Show supporting exception and timeline detail without competing with the main
  action flow
- Use a dedicated dashboard service layer for aggregation and prioritization
  logic
- Handle empty state cleanly when no processed reports exist
- Add or update backend tests for dashboard service and dashboard view behavior
- Update local documentation to reflect dashboard behavior and delivery-state
  truth

### Not Included

- Upload/parsing integration changes
- Automatic actions, reminders, or workflow execution
- Authentication or permissions
- Filtering, search, pagination, or multi-report comparison
- React or SPA frontend work
- Charts or advanced visualization libraries
- PDF parsing expansion

## Acceptance Criteria

- [ ] `GET /dashboard/` returns `200 OK`
- [ ] When no processed reports exist, the dashboard renders a clean empty state
      without crashing
- [ ] The dashboard uses the latest persisted `ParsedReport`
- [ ] The page shows a KPI strip with core report totals and operational
      orientation metrics
- [ ] The page shows a deterministic `Fila de Prioridades` as the main action
      section
- [ ] The page shows `Carteira em Foco` ordered by action priority and open
      value
- [ ] The page shows `Cliente 360` as a downstream drilldown fed by
      `Carteira em Foco`
- [ ] The page may keep supporting sections such as `Excecoes Operacionais`,
      `Clientes em Evidencia`, and `Timeline de Entregas` as long as they do
      not replace the main queue and client-focus flow
- [ ] Business rules for prioritization live outside the template layer
- [ ] Dashboard behavior is covered by tests
- [ ] Implementation follows SRP engineering standards: separation of concerns,
      high cohesion, loose coupling, security-first defaults, and documentation
      continuity

## Technical Notes

- Prefer direct model access through Django ORM instead of calling the API over
  HTTP internally
- Keep dashboard business logic in a service layer, not in the template
- Keep the first version single-page and latest-report only
- Deterministic bucket logic may remain in the service even when the page
  renders a single prioritized queue table instead of visible bucket sections
- Consolidating practical worklist visibility into `Fila de Prioridades` is an
  accepted implementation direction for SRP-13

## Dependencies

- SRP-11 — Parsed Data Models must be Done
- SRP-12 — Processed Data Retrieval API must be Done

## Suggested Story Points

- 5

## Jira Subtask: SRP-35 – Create Dashboard Service Layer And Action Rules

## Parent Story

- SRP-13 – Basic Dashboard View

## Purpose

Build the dashboard service that aggregates the latest parsed report into
summary metrics, priority logic, client rows, focused drilldown, and supporting
dashboard payloads.

## Scope

- Create a dedicated dashboard service module
- Aggregate report totals and client totals
- Define deterministic action-signal rules
- Keep decision logic out of templates

## Deliverables

- dashboard service layer
- deterministic prioritization logic
- prepared payloads for queue, portfolio, drilldown, and support sections

## Acceptance Criteria

- [ ] Service returns summary, client rows, `worklist_rows`, and the prepared
      dashboard payload used by the page
- [ ] Prioritization and action rules are deterministic
- [ ] Client ordering uses action priority and open value
- [ ] Service remains separate from the view/template layer

## Technical Notes

- Files: `reports/services/dashboard_service.py`
- API impact: none
- Validation notes: keep parsing/format handling safe and non-fatal

## Dependencies

- SRP-12 must be Done

## Suggested Story Points

- 2

## Jira Subtask: SRP-36 – Add Dashboard View, Route, And Latest-Report Selection

## Parent Story

- SRP-13 – Basic Dashboard View

## Purpose

Expose the dashboard through a human-facing Django view that selects the latest
processed report and handles empty state cleanly.

## Scope

- Add dashboard route
- Add dashboard view
- Select latest `ParsedReport`
- Pass prepared dashboard context to template

## Deliverables

- dashboard view
- dashboard route

## Acceptance Criteria

- [ ] `GET /dashboard/` returns `200 OK`
- [ ] Latest `ParsedReport` is used when data exists
- [ ] Empty state renders when no processed reports exist
- [ ] View orchestration remains thin

## Technical Notes

- Files: `backend/srp/urls.py`, `reports/views.py`
- API impact: adds human-facing dashboard page
- Validation notes: no internal HTTP call to retrieval API

## Dependencies

- SRP-35 must be Done

## Suggested Story Points

- 1

## Jira Subtask: SRP-37 – Implement Dashboard Template And Operational Sections

## Parent Story

- SRP-13 – Basic Dashboard View

## Purpose

Render the dashboard as a single-page operational surface for daily sales
follow-up using a story-driven page structure.

## Scope

- Add KPI strip
- Add operational pressure section
- Add `Fila de Prioridades`
- Add `Carteira em Foco`
- Add downstream `Cliente 360`
- Add supporting sections when they help inspection without competing with the
  main action flow
- Add empty state presentation

## Deliverables

- dashboard template

## Acceptance Criteria

- [ ] KPI strip is rendered
- [ ] Main priority queue is rendered
- [ ] Client portfolio section is rendered
- [ ] Focused client drilldown is rendered
- [ ] Supporting detail remains secondary to the queue and client-priority flow
- [ ] Template focuses on presentation rather than business rules

## Technical Notes

- Files: `reports/templates/reports/dashboard.html`
- API impact: none
- Validation notes: mobile-friendly enough for MVP and no fancy UI dependencies

## Dependencies

- SRP-36 must be Done

## Suggested Story Points

- 1

## Jira Subtask: SRP-38 – Add Dashboard Tests And Sync Documentation

## Parent Story

- SRP-13 – Basic Dashboard View

## Purpose

Validate the dashboard behavior and keep SRP documentation aligned with the
implemented dashboard and engineering standards.

## Scope

- Add dashboard service tests
- Add dashboard view tests
- Update README and AI context when dashboard behavior changes project truth
- Keep delivery-state documentation aligned

## Deliverables

- dashboard tests
- updated local docs

## Acceptance Criteria

- [ ] Dashboard service behavior is covered by tests
- [ ] Dashboard view behavior is covered by tests
- [ ] Empty and populated states are validated
- [ ] Local docs reflect the dashboard and delivery-state truth

## Technical Notes

- Files: `reports/tests/test_dashboard_service.py`,
  `reports/tests/test_dashboard_view.py`, `README.md`,
  `docs/AI/AI_CONTEXT_SRP.md`
- API impact: none
- Validation notes: documentation continuity is part of the definition of done

## Dependencies

- SRP-37 must be Done

## Suggested Story Points

- 1

## Suggested Jira Comment

`SRP-13 has been implemented locally through a story-driven operational dashboard flow. The remaining mismatch is primarily between the older exported backlog wording and the current tested implementation. Re-baseline SRP-13 and subtasks SRP-35 through SRP-38 to the implemented queue-centered dashboard, then move the story toward formal closure.`
