# SRP_13_IMPLEMENTATION_SLICES.md
## Purpose
Convert the recovered SRP-13 dashboard agreement into a practical sequence of
 implementation slices so the dashboard can be delivered in small, testable,
 story-aligned steps.
## Date
2026-04-23
## Author
Codex
## Domain
Systems / Sales Report Processor (SRP)

# SRP-13 Implementation Slices

## Decision Log

- 2026-04-23 — [systems] — Converted the reconciled dashboard agreement into an
  ordered slice plan so SRP-13 can move from documentation alignment into
  controlled implementation.
- 2026-04-23 — [systems] — Implemented `SRP-13-S1` locally: `Fila de
  Prioridades` now renders from `worklist_rows` and dashboard view coverage was
  updated to treat it as part of the page contract.
- 2026-04-23 — [systems] — Implemented `SRP-13-S2` locally: the current alert
  cards were moved into a dedicated support section so they no longer compete
  with `Fila de Prioridades` as the main action surface.
- 2026-04-23 — [systems] — Refined the support-layer direction: the current
  support section is acceptable as an intermediate state, but the preferred
  final form is one or more compact row-based support tables rather than a
  permanent multi-card support strip.
- 2026-04-23 — [systems] — Implemented `SRP-13-S3` locally: `Carteira em
  Foco` now renders as a client-priority section and `client_rows` are ordered
  by business priority instead of alphabetical name order.
- 2026-04-23 — [systems] — Implemented `SRP-13-S4` locally: `Sinais de Apoio`
  now renders as compact support tables for operational exceptions and client
  visibility instead of a multi-card strip.
- 2026-04-23 — [systems] — Refined the post-`S4` story flow locally:
  `Excecoes Operacionais` now appears before `Fila de Prioridades` as a
  pressure-explaining section, while `Clientes em Evidencia` now appears after
  `Carteira em Foco` as complementary client context.
- 2026-04-24 — [systems] — Implemented `SRP-13-S5` locally: `Cliente 360`
  now follows the first-ranked `Carteira em Foco` account explicitly and
  explains the handoff from portfolio priority into drilldown context.
- 2026-04-24 — [systems] — Implemented `SRP-13-S6` locally: local delivery
  docs now describe the shipped story-driven dashboard flow instead of the
  earlier mid-implementation state.
- 2026-04-24 — [systems] — Added `SRP_13_CLOSURE_RECOMMENDATION.md` to record
  the local decision that SRP-13 should be closed through backlog/export
  re-baselining rather than by forcing the dashboard back toward older wording.
- 2026-04-24 — [systems] — Added `SRP_13_BACKLOG_REBASE_DRAFT.md` with
  Jira-ready replacement wording for SRP-13 and subtasks SRP-35 through
  SRP-38 so closure sync can proceed concretely.

## Planning Goal

The goal is not to redesign the whole dashboard in one pass.

The goal is to move the current implementation from:

- KPI + operational charts + compact alert cards + `Cliente 360` + timeline

to:

- KPI + `Visao Operacional` + `Fila de Prioridades` + `Carteira em Foco` +
  `Cliente 360` + supporting detail

using the smallest valid sequence of changes.

## Planning Rules

- one slice must produce a visible improvement
- one slice must remain testable on its own
- do not rebuild stable sections unnecessarily
- preserve MVP simplicity
- prefer using the existing service payload before inventing new structures
- only add new service fields when the agreed section contract truly needs them

## Slice Order Overview

1. `SRP-13-S1` — Render `Fila de Prioridades` as the central action surface
2. `SRP-13-S2` — Reposition current alert cards as supporting summaries
3. `SRP-13-S3` — Build `Carteira em Foco` with business-priority ordering
4. `SRP-13-S4` — Convert support summaries into compact row-based support tables
5. `SRP-13-S5` — Align `Cliente 360` to the new reading flow
6. `SRP-13-S6` — Reconcile tests and delivery-state docs

## SRP-13-S1 — Render Fila de Prioridades

### Objective

Introduce the main action table so the dashboard finally answers:

- what should I do first?

### Why first

- This is the agreed center of the page
- Existing service data already exposes most of the needed item-level fields
- It reduces the largest gap between current implementation and agreed
  dashboard direction

### In-scope

- add a visible `Fila de Prioridades` section after `Visao Operacional`
- render rows from `worklist_rows`
- show the core columns already agreed:
  - prioridade
  - flag principal
  - cliente
  - pedido / seq
  - material
  - prazo
  - motivo
  - acao sugerida
- include optional operational fields only if they improve scanning:
  - OP
  - sit. ordem
  - sit. item

### Likely files

- `backend/reports/templates/reports/dashboard.html`
- `backend/reports/tests/test_dashboard_view.py`

### Service dependency check

Use existing `worklist_rows` fields first:

- `priority_label`
- `primary_bucket_label`
- `customer_name`
- `pedido`
- `seq`
- `description`
- `dt_entr`
- `reason_text`
- `next_action`
- `ord_prod`
- `sit_ordem`
- `sit`

### Acceptance target

- `Fila de Prioridades` is visible on the page
- the section is clearly the main action surface
- rows are rendered in service order
- the user can understand why each row matters and what to do next

### Out of scope for this slice

- final client portfolio redesign
- final alert-card removal
- large service refactor

## SRP-13-S2 — Reposition Current Alert Cards

### Objective

Keep useful alert summaries without letting them remain the main action surface.

### Why second

- once the queue exists, the cards need a new role
- this avoids duplicating the same action signal in too many places

### In-scope

- demote `Bloqueio de Credito`
- demote `Entrega em Atencao`
- demote `Cliente de Alto Valor`
- demote `Clientes com Flags`
- move them into a clear supporting area or compact summary zone
- ensure they visually support the queue rather than compete with it

### Likely files

- `backend/reports/templates/reports/dashboard.html`
- `backend/reports/tests/test_dashboard_view.py`

### Acceptance target

- cards still exist only if they help summary scanning
- the user no longer needs the cards to understand the core queue
- the page reads as:
  - pressure first
  - action queue second
  - supporting summaries after
- this slice is allowed to remain card-based temporarily while the support layer
  is later converted into row-based support tables

## SRP-13-S3 — Build Carteira em Foco

### Objective

Add the client-priority section that answers:

- which accounts deserve concentrated attention?

### Why third

- this section depends on the action-centered reading already being established
- current service output needs some business-priority enrichment first

### In-scope

- add `Carteira em Foco` after `Fila de Prioridades`
- render one row per client
- sort by:
  1. action priority
  2. flag count
  3. open value
  4. client name
- enrich client rows if needed with:
  - dominant concern
  - short focus reason
  - next reading cue

### Likely files

- `backend/reports/services/dashboard_service.py`
- `backend/reports/templates/reports/dashboard.html`
- `backend/reports/tests/test_dashboard_service.py`
- `backend/reports/tests/test_dashboard_view.py`

### Current known gap

- `client_rows` are currently sorted alphabetically
- that does not match the agreed business reading of `Carteira em Foco`

### Acceptance target

- `Carteira em Foco` is visibly distinct from the item queue
- account rows are ordered by business priority rather than name
- each row explains why the client deserves attention now

## SRP-13-S4 — Convert Support Summaries Into Row-Based Support Tables

### Objective

Replace the current multi-card support layer with one or more compact support
tables that make comparison easier without competing with the main queue.

### Why fourth

- once `Carteira em Foco` exists, the dashboard will have enough primary
  structure to reshape the support layer cleanly
- row-based support tables better fit the agreed storytelling model than
  separate mini-cards

### In-scope

- replace the current support cards with one or more compact support tables
- likely group support into:
  - operational exceptions
  - client-support visibility
- keep support explicitly secondary to:
  - `Fila de Prioridades`
  - `Carteira em Foco`

### Likely files

- `backend/reports/templates/reports/dashboard.html`
- `backend/reports/tests/test_dashboard_view.py`
- optionally `backend/reports/services/dashboard_service.py` if small support
  reshaping is needed

### Acceptance target

- support data becomes easier to compare row by row
- the support layer remains useful without returning to a card-heavy action
  surface
- the page reads as pressure context first, queue second, and complementary
  client support later

## SRP-13-S5 — Align Cliente 360

### Objective

Make `Cliente 360` behave as a downstream drilldown instead of a parallel
centerpiece.

### Why fifth

- the right client context only makes sense after the queue and client portfolio
  sections exist

### In-scope

- confirm which client should feed `Cliente 360`
- align the section to the new reading flow:
  - `Carteira em Foco` -> `Cliente 360`
- keep the section focused on action-enabling context:
  - portfolio summary
  - active flags
  - critical items

### Likely files

- `backend/reports/services/dashboard_service.py`
- `backend/reports/templates/reports/dashboard.html`
- `backend/reports/tests/test_dashboard_service.py`
- `backend/reports/tests/test_dashboard_view.py`

### Acceptance target

- `Cliente 360` reads as drilldown, not as a competing primary section
- the chosen client feels consistent with the dashboard’s priority logic

## SRP-13-S6 — Reconcile Tests and Delivery-State Docs

### Objective

Close the gap between implementation, tests, and local delivery truth.

### Why last

- documentation and tests should reflect the final section structure, not an
  intermediate draft

### In-scope

- update view tests for the final page sections
- update service tests if service ordering or enrichment changes
- sync local docs:
  - `README.md`
  - `docs/AI/AI_CONTEXT_SRP.md`
  - `docs/AI/SRP_13_DASHBOARD_AGREED_SCOPE.md`
  - this slice plan if needed

### Likely files

- `backend/reports/tests/test_dashboard_service.py`
- `backend/reports/tests/test_dashboard_view.py`
- `README.md`
- `docs/AI/AI_CONTEXT_SRP.md`
- `docs/AI/SRP_13_DASHBOARD_AGREED_SCOPE.md`

### Acceptance target

- tests assert the story-driven dashboard structure
- docs no longer describe the dashboard as merely "being implemented"
- local delivery state is no longer ambiguous

## Immediate Next Slice

### Recommended next move

- Treat the SRP-13 slice plan as complete locally and move to closure/package work

### Reason

- the implementation slices are now complete locally
- the next remaining work is no longer feature construction inside SRP-13
- delivery state should be reconciled against backlog/export authority and then
  packaged for the next ticket transition
- `docs/AI/SRP_13_CLOSURE_RECOMMENDATION.md` is now the primary local closure
  note for that re-baselining step
- `docs/AI/SRP_13_BACKLOG_REBASE_DRAFT.md` now provides the replacement Jira
  wording for that sync step

### Working instruction for the next implementation session

`Close the local SRP-13 implementation cycle by reconciling backlog/export state and preparing the project for the next delivery transition.`
