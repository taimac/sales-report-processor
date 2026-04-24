# SRP_13_DASHBOARD_AGREED_SCOPE.md
## Purpose
Preserve the durable SRP-13 dashboard design rationale without turning this
file into a second ticket tracker or competing backlog authority.
## Date
2026-04-23
## Author
Codex
## Domain
Systems / Sales Report Processor (SRP)

# SRP-13 Dashboard Agreed Scope

## Status

This file is retained as historical design rationale only.

It is **not** the source of truth for:

- current ticket status
- next ticket selection
- official acceptance criteria
- closure state

Those belong to Jira and the exported backlog in `docs/jira_backlog_SRP.md`.

## Decision Log

- 2026-04-23 — [systems] — Recovered the agreed dashboard direction from the
  working notes, backlog story, README, and current test-backed implementation.
  This file is the clean agreement summary; the working notes remain the full
  discussion trace.
- 2026-04-23 — [systems] — Added the explicit dashboard storytelling model:
  the page should guide the user from overall carteira context to operational
  pressure, then to a concrete priority queue, and finally into client-level
  inspection and supporting detail.
- 2026-04-23 — [systems] — Locked a sharper working spec for `Fila de
  Prioridades` and `Carteira em Foco` so the dashboard can be refined against a
  concrete section contract instead of broad intent only.
- 2026-04-23 — [systems] — Added reconciled SRP-13 acceptance criteria to
  align the backlog story with the recovered dashboard direction and the
  current implementation baseline.
- 2026-04-23 — [systems] — Refined the support-layer decision: the final
  `Sinais de Apoio` direction should prefer compact row-based support tables
  over separate mini-cards when the goal is to compare multiple rows of
  exception or client-support data.

## Sources Used

- `docs/jira_backlog_SRP.md` (`SRP-13`)
- `README.md`
- `backend/reports/tests/test_dashboard_view.py`
- `backend/reports/tests/test_dashboard_service.py`

## What Was Clearly Agreed

### 1. Dashboard role

- The dashboard should behave as an action console, not as a passive summary
  page.
- The page should help answer:
  - what needs attention now
  - which clients or orders are at risk or stuck
  - what volume is still open vs in production vs invoiced
  - where the sales rep should follow up first
- The page remains MVP-simple:
  - Django template based
  - read-only
  - latest-report only
  - no React
  - no workflow automation actions
  - no parser expansion

### 2. Top section: KPI strip

- The top KPI strip was considered mostly stable in the working discussion.
- It should stay concise and focused on commercial and delivery management.
- The stable KPI set across context, README, and implementation is:
  - `Total de Clientes`
  - `Pedidos em Atraso`
  - `Produzido Com Data Vencida`
  - `Peso em Atraso`
  - `Falta Produzir`
  - `Entrega Esse Mes`
  - `Saldo em Estoque`
  - `Faturado`
  - `Valor em Pedidos`
  - `Quantidade Pedida`
  - `Preco Medio`

### 3. Second section: Visao Operacional

- `Visao Operacional` is a kept section and was described as moving in the
  right direction.
- Its job is to show where pressure is concentrated, not just display totals.
- The agreed operational emphasis is chart-led and centered on:
  - overdue order-line pressure versus total lines
  - overdue remaining demand by client
  - overdue produced stock by client
  - overdue commercial value by client

### 4. Page flow

- The agreed page should tell a structured operational story in this order:
  1. `Top KPIs`
  2. `Visao Operacional`
  3. `Fila de Prioridades`
  4. `Carteira em Foco`
  5. `Cliente 360 / Drilldown`
  6. `Apoio / Detalhes`
- The page should move from executive context to operational pressure to direct
  action cues and only then into inspection detail.

## Storytelling Model

### Core principle

- The dashboard should tell a story, not just display information blocks.
- That story should behave like an operational briefing:
  - first explain the overall state of the carteira
  - then reveal where pressure is concentrated
  - then show what needs action now
  - then give enough context to act on the right client or order

### The story the page should tell

#### 1. "What is the situation overall?"

- This is the job of `Top KPIs`.
- It provides fast executive orientation:
  - size of the carteira
  - amount overdue
  - amount still to produce
  - current stock, invoiced volume, and order value
- The goal is not deep diagnosis yet.
- The goal is to let the user understand the state of the report in a few
  seconds.

#### 2. "Where is the pressure concentrated?"

- This is the job of `Visao Operacional`.
- It should show where the system is under tension:
  - which share of lines is overdue
  - which clients concentrate delay
  - where produced stock is sitting with overdue delivery
  - where commercial value is at risk
- This is the bridge between summary and action.
- It explains why the next queue matters.

#### 3. "What should I do first?"

- This is the job of `Fila de Prioridades`.
- This is the narrative turning point of the dashboard.
- Instead of forcing the user to interpret several disconnected cards, the page
  should surface a visible work queue ordered by urgency and relevance.
- Every row in this section should answer:
  - why this item matters now
  - what signal triggered it
  - what commercial or operational action is implied next

#### 4. "Which accounts deserve attention first?"

- This is the job of `Carteira em Foco`.
- After the priority queue identifies immediate work, this section should help
  the user see which clients deserve sustained attention because of:
  - open value
  - concentration of flags
  - delivery exposure
  - broader carteira importance
- This section is more account-oriented than item-oriented.

#### 5. "What do I need to know before acting on this client?"

- This is the job of `Cliente 360 / Drilldown`.
- It should give the user enough context to move from alert to follow-up:
  - what the client represents in the report
  - what is overdue or blocked
  - which rows are critical
  - what story explains the current exposure

#### 6. "What supporting detail is useful but not central?"

- This is the job of `Apoio / Detalhes`.
- These elements should support inspection without competing with the main
  decision flow.
- Examples may include:
  - timelines
  - secondary supporting tables
  - inspection aids
  - detail views that help confirm action, but do not define priority
- When support content is comparison-heavy, rows are preferred over separate
  cards.

### Story quality rule

- A good dashboard section is not included because it is available in the data.
- A section belongs on the page only if it advances the operational story.
- If a component does not help answer one of these questions:
  - what is happening
  - where is the pressure
  - what do I do now
  - what context do I need before acting
  it should be simplified, moved down, or removed.

### Practical implication for layout decisions

- The dashboard should not read like:
  - KPIs
  - random cards
  - a table
  - extra details
- It should read like:
  - situation
  - pressure
  - priorities
  - client focus
  - drilldown
  - support

### 5. Central section decision

- If one section becomes the center of the page, it should be
  `Fila de Prioridades`.
- The reason agreed in the discussion:
  - it converts flags into visible work
  - it supports business resolution more directly than isolated cards
  - it best matches the goal of an action-oriented dashboard

### 6. Fila de Prioridades intent

- The priority queue was agreed conceptually even though its final layout was
  not frozen.
- Suggested columns:
  - `Prioridade`
  - `Flag principal`
  - `Cliente`
  - `Pedido / Seq`
  - `Material`
  - `Qtd faltante`
  - `Valor / peso relevante`
  - `Prazo`
  - `Motivo`
  - `Acao sugerida`
- Suggested ordering:
  - severity and delivery proximity first
  - then commercial weight
  - then client relevance

## Fila de Prioridades Spec

### Section purpose

- `Fila de Prioridades` is the main action table of the dashboard.
- Its job is to convert operational signals into a visible work queue.
- It should answer one practical question:
  - what should the sales rep act on first, and why?

### Narrative role

- This section comes after `Visao Operacional` because the charts explain the
  pressure, and the queue translates that pressure into action.
- It should replace the need to scan multiple disconnected alert cards.

### Data source

- Primary source: `worklist_rows`
- Supporting context:
  - `action_counts`
  - report-level KPI and operational context when needed

### Recommended row granularity

- One row per actionable item.
- The row should stay item-level, not customer-level, because this is the
  section where the user decides what to do next on a specific order/material.

### Recommended columns

- `Prioridade`
  - display `priority_label`
- `Flag principal`
  - display `primary_bucket_label`
- `Cliente`
  - display `customer_name`
- `Pedido / Seq`
  - display `pedido` and `seq`
- `Material`
  - display `description`
- `Qtd faltante`
  - derived from open coverage logic
  - use the operational meaning of remaining delivery quantity
- `Valor / peso relevante`
  - use the most decision-useful business magnitude available for the row
  - prefer open balance / commercial exposure over decorative values
- `Prazo`
  - display `dt_entr` and/or `deadline_label`
- `Motivo`
  - display `reason_text`
- `Acao sugerida`
  - display `next_action`

### Recommended optional supporting columns

- `OP`
  - display `ord_prod`
- `Sit. Ordem`
  - display `sit_ordem`
- `Sit. Item`
  - display `sit`
- `Credito`
  - use `cr_pro` / `cr_fat` only when the row is credit-related

### Sorting rule

- Sort by:
  1. `priority_score` descending
  2. `customer_open_value` descending
  3. `open_balance_value` descending
  4. client and order tie-breakers
- This matches the current service behavior and is consistent with the agreed
  logic:
  - severity first
  - then commercial weight
  - then client relevance

### Row content rule

- Every row must make the urgency legible without requiring the user to infer
  it from several sections.
- A row is good if the user can scan it and answer:
  - why is this row here?
  - what is the main risk?
  - what should I do next?

### Design rule

- `Fila de Prioridades` should absorb most of the practical visibility now split
  across:
  - `Bloqueio de Credito`
  - `Entrega em Atencao`
  - `Cliente de Alto Valor`
  - `Clientes com Flags`
- Those cards may remain as supporting summaries, but the queue should become
  the primary working surface.
- In the longer-term direction, those support summaries should preferably be
  consolidated into one or more compact row-based support tables.

## Carteira em Foco Spec

### Section purpose

- `Carteira em Foco` is the account-priority section of the dashboard.
- Its job is to show which customers deserve sustained attention beyond the
  item-level queue.
- It should answer:
  - which accounts are commercially most important to watch right now?

### Narrative role

- This section comes after `Fila de Prioridades`.
- The queue says what needs action now.
- `Carteira em Foco` says which client relationships deserve concentration and
  follow-up energy.

### Data source

- Primary source: `client_rows`
- Supporting enrichment:
  - client-level flag summaries derived from item signals
  - high-value exposure logic
  - actionable item counts

### Recommended row granularity

- One row per client.
- This section is client-level, not order-level.

### Recommended columns

- `Cliente`
  - display `customer_name`
- `Representante`
  - display `representative`
- `Valor da carteira`
  - display `total_valor`
- `Saldo em aberto`
  - display `total_sdo`
- `Qtd de flags`
  - display `action_flag_count`
- `Prioridade da conta`
  - display or derive from `action_priority`
- `Principal sinal`
  - show the dominant client-level concern
  - for example: atraso, credito, falta de OP, alto valor
- `Motivo de foco`
  - short text explaining why this client belongs near the top
- `Proxima leitura`
  - short cue such as "abrir Cliente 360", "revisar itens vencidos",
    "validar credito", or "cobrar programacao"

### Sorting rule

- This section should be ordered by:
  1. `action_priority` descending
  2. `action_flag_count` descending
  3. open value descending
  4. client name as final tie-breaker
- This is intentionally different from the current alphabetical `client_rows`
  sort in the service.
- The page agreement favors business priority ordering over neutral name order.

### Row content rule

- A client row should explain why the account matters now, not only how large
  it is.
- High value alone is not enough.
- A client belongs near the top when wallet importance and operational risk
  reinforce each other.

### Relationship to Cliente 360

- `Carteira em Foco` is a portfolio-level ranking.
- `Cliente 360` is the inspection view for one selected account.
- The expected reading flow is:
  - notice the account in `Carteira em Foco`
  - then open or inspect that account through `Cliente 360`

## Difference Between The Two Sections

### Fila de Prioridades

- unit of attention: item / order line
- question answered: what should I act on first?
- orientation: immediate action
- best for: urgency, queueing, next step

### Carteira em Foco

- unit of attention: client / account
- question answered: which accounts deserve concentrated attention?
- orientation: relationship and exposure management
- best for: follow-up planning, commercial focus, escalation context

## Implementation Alignment Note

- The current service already exposes most of what `Fila de Prioridades`
  requires through `worklist_rows`.
- The current service only partially matches the desired `Carteira em Foco`
  behavior because `client_rows` are still alphabetically ordered.
- That means the queue spec is close to implementation-ready, while the client
  portfolio section still needs explicit alignment to the agreed business
  ordering.

## Reconciled SRP-13 Acceptance Criteria

These criteria replace the older "queue + table + worklist" reading of SRP-13
with a story-driven contract that still respects the original story goal:
turn persisted parsed data into practical daily sales priorities.

### A. Base delivery criteria

- [ ] `GET /dashboard/` returns `200 OK`
- [ ] When no processed reports exist, the dashboard renders a clean empty state
      without crashing
- [ ] The dashboard uses the latest persisted `ParsedReport`
- [ ] Dashboard aggregation and prioritization logic live in a dedicated service
      layer, not in the template
- [ ] Dashboard behavior is covered by backend tests

### B. Storytelling criteria

- [ ] The page reads as an operational story, not as disconnected widgets
- [ ] The section flow is visibly ordered as:
      `Top KPIs` -> `Visao Operacional` -> `Fila de Prioridades` ->
      `Carteira em Foco` -> `Cliente 360 / Drilldown` -> `Apoio / Detalhes`
- [ ] Each primary section answers a distinct question:
      - `Top KPIs`: what is the situation overall?
      - `Visao Operacional`: where is the pressure concentrated?
      - `Fila de Prioridades`: what should I do first?
      - `Carteira em Foco`: which accounts deserve attention?
      - `Cliente 360 / Drilldown`: what context is needed before acting?
- [ ] Supporting sections do not compete with the core action flow

### C. Top KPI criteria

- [ ] The page shows a concise KPI strip that explains the report’s overall
      commercial and delivery state
- [ ] The KPI strip includes the stabilized indicators:
      - total clients
      - overdue orders
      - produced with overdue delivery
      - overdue weight
      - remaining to produce
      - delivery this month
      - stock balance
      - invoiced total
      - total report value
      - total ordered quantity
      - average price
- [ ] The KPI strip supports orientation first and does not attempt to replace
      the priority queue

### D. Visao Operacional criteria

- [ ] The page shows `Visao Operacional` immediately after the KPI strip
- [ ] This section makes concentration of pressure legible through operational
      views such as:
      - overdue line pressure
      - overdue remaining demand by client
      - overdue produced stock by client
      - overdue commercial value by client
- [ ] This section explains why subsequent priorities matter

### E. Fila de Prioridades criteria

- [ ] `Fila de Prioridades` is the main action section of the page
- [ ] It is rendered from item-level actionable data derived from
      `worklist_rows`
- [ ] It is ordered by business priority, using the agreed logic:
      - severity first
      - then commercial weight
      - then client relevance
- [ ] Each row clearly expresses:
      - priority
      - main flag
      - client
      - order / sequence
      - material
      - remaining quantity or equivalent operational gap
      - relevant business magnitude
      - deadline or delivery cue
      - reason
      - suggested next action
- [ ] The user can understand why a row is present and what action it implies
      without cross-reading multiple cards
- [ ] The queue absorbs most of the practical visibility previously scattered
      across isolated alert cards

### F. Carteira em Foco criteria

- [ ] `Carteira em Foco` is rendered as a client-level portfolio section after
      `Fila de Prioridades`
- [ ] It is built from client-level data derived from `client_rows`
- [ ] It is ordered by account importance and operational urgency, not by
      alphabetical name order
- [ ] Each row explains why the client deserves attention now through a
      combination of:
      - open value
      - open balance
      - flag count
      - account priority
      - dominant concern
      - short focus rationale
- [ ] This section helps the user decide which accounts deserve concentrated
      follow-up beyond the immediate item queue

### G. Cliente 360 criteria

- [ ] `Cliente 360 / Drilldown` remains a downstream inspection section, not
      the center of the page
- [ ] It gives enough context to act on a focused client:
      - portfolio summary
      - active flags
      - critical items or rows
- [ ] The expected reading flow is:
      `Carteira em Foco` -> `Cliente 360`

### H. Apoio / Detalhes criteria

- [ ] Supporting sections such as delivery timeline or secondary detail views
      may remain on the page
- [ ] These sections support inspection and confirmation, but do not replace
      `Fila de Prioridades` or `Carteira em Foco`
- [ ] When support content needs side-by-side comparison across multiple items
      or multiple clients, it should prefer compact row-based tables rather than
      separate cards
- [ ] Support presentation should optimize scanability and comparison, not
      decorative separation
- [ ] If a supporting block does not advance the dashboard story, it should be
      simplified, demoted, or removed

### I. Transition criteria for current implementation

- [ ] The current card set may remain temporarily as supporting summaries while
      the queue-centered layout is being finalized
- [ ] `Bloqueio de Credito`, `Entrega em Atencao`, `Cliente de Alto Valor`, and
      `Clientes com Flags` should no longer be treated as the primary action
      surface once `Fila de Prioridades` is in place
- [ ] The preferred end state for the support layer is one or more compact
      row-based support tables, not a permanent four-card support strip
- [ ] The final SRP-13 closure should reflect the agreed queue-centered and
      portfolio-centered reading of the dashboard, not only the earlier
      card-based implementation

## Current Baseline Against The Reconciled Criteria

### Already satisfied in the current implementation

- dashboard route exists
- latest-report selection exists
- empty state exists
- KPI strip exists
- `Visao Operacional` exists
- `Excecoes Operacionais` exists before `Fila de Prioridades`
- `Fila de Prioridades` exists as the main queue section
- `Carteira em Foco` exists as a distinct account-priority section
- `client_rows` are ordered by business priority rather than alphabetical name
- service-layer aggregation exists
- backend dashboard tests exist
- `Clientes em Evidencia` exists as a complementary client-support section
- `Cliente 360` exists and now follows the first-ranked `Carteira em Foco`
  account explicitly
- supporting delivery timeline exists
- supporting visibility is rendered as row-based tables rather than the earlier
  card strip

### Not yet clearly aligned with the reconciled criteria

- backlog/export wording and local delivery-state records still need closure
  synchronization
- SRP-13 still needs formal closure against the authoritative backlog state,
  even though the local implementation now matches the recovered direction

### 7. Cards that were likely transitional

- The isolated cards below were identified as candidates to be replaced or
  absorbed into a stronger action-oriented table:
  - `Bloqueio de Credito`
  - `Entrega em Atencao`
  - `Cliente de Alto Valor`
  - `Clientes com Flags`
- The refined support-layer direction is:
  - `Bloqueio de Credito` + `Entrega em Atencao` are strong candidates for one
    compact exception table
  - `Cliente de Alto Valor` + `Clientes com Flags` are strong candidates for
    one compact client-support table

## Accepted Flag Model

### Stable flags

- `credit_block`
  - commercial credit restriction
  - applies at item and client level
- `delivery_attention`
  - delivery date near or overdue
  - remaining delivery quantity still positive
  - applies at item and client level
- `missing_production_reference`
  - relevant near-delivery row without usable OP/reference
  - applies at item and client level
- `high_value_customer`
  - customer is among the highest-value open exposures
  - applies at client level
- `coverage_excess`
  - invoiced quantity plus stock exceeds ordered quantity
  - indicates possible data inconsistency or coverage distortion
  - applies at item and client level

### Working but not frozen

- `production_follow_up`
  - stays active as a broader operational signal for now
  - exact final trigger was intentionally left open

### Explicitly de-emphasized

- `stock_balance`
  - should not stand alone as its own flag for now
  - it overlaps too much with production follow-up logic

## Agreed Formulas

- `remaining_delivery_qty = qt_ped - qt_fatur - sdo_estoq`
- `coverage_qty = qt_fatur + sdo_estoq`

### Accepted uses

- `delivery_attention` should use `remaining_delivery_qty > 0`
- `coverage_excess` should use `coverage_qty > qt_ped`

## What Was Not Finalized

- the stricter final rule for `production_follow_up`
- the exact severity scoring formula
- the final dashboard table layout
- the next extra insights to add inside `Visao Operacional`
- the exact split between `Carteira em Foco` and `Cliente 360`
- what should live under `Apoio / Detalhes`

## Current Implementation Snapshot

The current codebase already renders a dashboard with:

- `Indicadores Principais`
- `Visao Operacional`
- `Excecoes Operacionais`
- `Fila de Prioridades`
- `Carteira em Foco`
- `Clientes em Evidencia`
- `Cliente 360`
- `Timeline de Entregas`

The current test-backed implementation also shows that:

- `Fila de Prioridades` is currently rendered
- `Carteira em Foco` is currently rendered
- `Clientes em Evidencia` is currently rendered
- `Cliente 360` now receives an explicit handoff from `Carteira em Foco`
- `Rankings` is not currently rendered
- `Matriz de Flags` is not currently rendered
- the support layer is rendered as row-based exception and client-support tables

## Practical Interpretation

- The repo appears to be between two states:
  - an earlier card-based operational dashboard that is already implemented
  - a later agreed direction where `Fila de Prioridades` becomes the page
    center and absorbs much of the current card visibility
- Because of that, this file should be treated as the best recovered statement
  of agreement about what belongs on the dashboard, not as proof that SRP-13 is
  fully reconciled with backlog acceptance wording.

## Recommended Resume Point

Resume the next SRP closure discussion in this order:

1. reconcile the final agreed dashboard shape with backlog/export wording
2. confirm whether SRP-13 is ready for formal closure in project tracking
3. package the MVP dashboard path for the next ticket transition
