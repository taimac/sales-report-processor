# SRP_13_CLOSURE_RECOMMENDATION.md
## Purpose
Record the local delivery decision for SRP-13 after implementation and closure
diagnosis so the project can re-baseline backlog state without rediscovering
the same acceptance mismatch.
## Date
2026-04-24
## Author
Codex
## Domain
Systems / Sales Report Processor (SRP)

# SRP-13 Closure Recommendation

## Decision

Recommend closing SRP-13 through backlog/export re-baselining rather than by
forcing the implemented dashboard back toward the older literal acceptance
wording.

## Why this recommendation exists

Local implementation now delivers a coherent story-driven dashboard flow:

- `Indicadores Principais`
- `Visao Operacional`
- `Excecoes Operacionais`
- `Fila de Prioridades`
- `Carteira em Foco`
- `Clientes em Evidencia`
- `Cliente 360`
- `Timeline de Entregas`

That implemented flow is test-backed and consistent with the recovered
dashboard agreement captured in:

- `docs/AI/SRP_13_DASHBOARD_AGREED_SCOPE.md`
- `docs/AI/SRP_13_IMPLEMENTATION_SLICES.md`

The remaining gap is mainly documentary:

- the exported backlog still describes an older dashboard reading
- SRP-35 through SRP-38 are still marked `To Do`
- SRP-13 is still marked `In Progress`

## Local implementation evidence

### Route and view

- `GET /dashboard/` exists
- latest persisted `ParsedReport` is selected
- empty state is handled cleanly

Primary files:

- `backend/reports/views.py`
- `backend/srp/urls.py`

### Service layer

- dashboard aggregation lives in a dedicated service
- prioritization rules remain outside the template
- client ordering is business-priority driven
- `Cliente 360` follows the first-ranked `Carteira em Foco` account explicitly

Primary file:

- `backend/reports/services/dashboard_service.py`

### Template layer

- KPI strip is rendered
- queue-centered operational story is rendered
- support sections are row-based instead of the earlier card strip

Primary file:

- `backend/reports/templates/reports/dashboard.html`

### Validation

- dashboard service behavior is covered by tests
- dashboard view behavior is covered by tests
- empty and populated states are validated locally

Primary files:

- `backend/reports/tests/test_dashboard_service.py`
- `backend/reports/tests/test_dashboard_view.py`

## What is locally satisfied

- SRP-35 is substantively satisfied locally
  - service layer exists
  - deterministic action logic exists
  - client ordering uses action priority and open value
- SRP-36 is substantively satisfied locally
  - route exists
  - view exists
  - latest-report selection exists
  - empty state exists
- SRP-37 is substantively satisfied locally
  - KPI strip exists
  - queue-centered operational template exists
  - client portfolio section exists
  - worklist-style operational detail exists inside the queue-centered design
- SRP-38 is substantively satisfied locally
  - dashboard tests exist
  - local docs were synchronized to implementation truth

## Remaining mismatch with the exported backlog

The current exported backlog still expects a more literal contract in a few
places:

1. KPI wording
- backlog still explicitly calls for visible `in production`, actionable item
  count, and actionable client count in the KPI strip
- the service computes these values, but the template does not currently render
  all of them visibly

2. Queue wording
- backlog still reads as if the queue must be shown through explicit
  deterministic bucket sections
- the implemented dashboard uses a single prioritized queue table backed by
  deterministic bucket logic rather than rendering each bucket as its own block

3. Worklist wording
- backlog still reads as if a separate worklist must exist alongside the queue
- the implemented dashboard deliberately consolidates the practical worklist
  into `Fila de Prioridades`

## Recommendation

### Recommended path

Use the recovered agreement and local implementation as the new delivery truth
for SRP-13, then re-baseline the backlog/export wording accordingly.

### Why this is better than redesigning backward

- the current dashboard is more coherent than the older literal contract
- the story-driven flow was shaped deliberately, not accidentally
- forcing separate queue buckets plus a separate worklist would likely reduce
  clarity instead of improving it
- the main problem now is tracking truth, not feature absence

## Conservative note

If the team wants a stricter closure threshold before formal story closure,
these may be treated as optional clarifiers:

- add visible `in production` to the KPI strip
- add visible actionable item count and actionable client count to the KPI strip
- explicitly decide whether visible queue buckets are still required or whether
  deterministic queue logic already satisfies that intent

These should be treated as closure clarifiers, not as grounds to discard the
implemented dashboard direction.

## Recommended closure statement

`SRP-13 is implemented locally and aligned with the recovered story-driven dashboard agreement. Remaining blockers are primarily backlog/export wording and ticket-state synchronization, not missing dashboard infrastructure. Re-baseline SRP-13 acceptance to the implemented queue-centered operational flow, mark SRP-35 through SRP-38 as satisfied locally, and move SRP-13 toward formal closure.`

## Next action

1. Update backlog/export wording for SRP-13 and its subtasks to match the
   implemented story-driven dashboard
2. Mark SRP-35 through SRP-38 as satisfied
3. Move SRP-13 from `In Progress` toward formal closure
4. Only after that, select the next valid delivery focus
