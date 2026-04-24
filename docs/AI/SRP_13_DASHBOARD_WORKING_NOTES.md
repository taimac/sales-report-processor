# SRP_13_DASHBOARD_WORKING_NOTES.md
## Purpose
Preserve the current SRP-13 dashboard discussion so the next session can resume
from the latest agreed dashboard model without rediscovery.
## Date
2026-04-18
## Author
Codex
## Domain
Systems / Sales Report Processor (SRP)

# SRP-13 Dashboard Working Notes

## Status

Working discussion snapshot for `SRP-13 - Basic Dashboard View`.

This note captures the agreed dashboard flag model and the exact point where the
discussion stopped on 2026-04-18.

Use this as the immediate reference before refining dashboard structure or
implementing further dashboard behavior.

## Working Context

- The dashboard is being shaped manually against business usefulness, not by
  strict backlog literalism.
- The current guiding question is:
  `does this screen surface useful information capable of triggering business action?`
- Top KPIs are considered mostly stable for now.
- `Visao Operacional` is moving in the right direction, but remains open to
  additional useful insights.
- The next major dashboard design discussion should start after the flag model,
  not by reopening KPI-strip debate.

## Agreed Dashboard Direction

- Treat the dashboard more as an action console than a passive summary page.
- Keep the KPI strip concise and focused.
- Improve the visibility of operational issues in the middle section.
- Consider replacing or consolidating isolated cards such as:
  - `Bloqueio de Credito`
  - `Entrega em Atencao`
  - `Cliente de Alto Valor`
  - `Clientes com Flags`
  into a more visible action-oriented table section.

## Accepted Flag Model

### 1. `credit_block`

- Level: `item`, `client`
- Trigger: credit restriction present in the commercial/financial fields
- Meaning: the row is commercially blocked regardless of other progress
- Status: accepted

### 2. `delivery_attention`

- Level: `item`, `client`
- Trigger:
  - delivery date `< 10 days`
  - `qt_ped - qt_fatur - sdo_estoq > 0`
- Meaning:
  the client still expects quantity that is neither invoiced nor already
  covered by available stock
- Recommended row display:
  - `remaining_delivery_qty = qt_ped - qt_fatur - sdo_estoq`
- Status: accepted

### 3. `production_follow_up`

- Level: `item`, `client`
- Working trigger:
  keep the current broader operational logic for now
- Additional display intent:
  the row should make clear how much is still missing for delivery coverage
- Status: intentionally left broad for now

### 4. `missing_production_reference`

- Level: `item`, `client`
- Trigger:
  - relevant row
  - no usable production reference / OP
  - delivery date `< 10 days`
- Meaning:
  the row is near delivery and lacks production traceability
- Status: accepted

### 5. `high_value_customer`

- Level: `client`
- Trigger:
  client is among the highest-value open exposures
- Meaning:
  commercial importance should amplify attention and ordering
- Status: accepted

### 6. `coverage_excess`

- Level: `item`, `client`
- Trigger:
  - `qt_fatur + sdo_estoq > qt_ped`
- Meaning:
  invoiced quantity plus available stock exceeds ordered quantity
- Risk:
  - data inconsistency
  - duplicated coverage interpretation
  - wrong pending/available reading
- Status: accepted

### 7. `stock_balance`

- Decision:
  do not keep as a standalone flag for now
- Reason:
  it overlaps too much with `production_follow_up`
- Status: absorbed into other operational logic

## Severity Model

Current working rule:

- severity is influenced by both:
  - flag type
  - delivery proximity

This model is accepted as a working rule, but not yet frozen into exact formula
or thresholds beyond the near-delivery logic above.

## Useful Formulas Agreed in Discussion

- `remaining_delivery_qty = qt_ped - qt_fatur - sdo_estoq`
- `coverage_qty = qt_fatur + sdo_estoq`

Current accepted use:

- `delivery_attention` should use `remaining_delivery_qty > 0`
- `coverage_excess` should use `coverage_qty > qt_ped`

## What Was Explicitly Deferred

- A stricter final formula for `production_follow_up`
- Exact severity scoring mechanics
- Final dashboard table layout
- Exact next additions inside `Visao Operacional`

These were intentionally left open to avoid over-freezing the dashboard too
early.

## Dashboard Principle

The dashboard should not behave like a passive summary page.

Current agreed framing:

- the dashboard should tell a structured operational history
- that history should help explain why a row matters now
- the page should provoke actionable decisions, not just display totals

This means the page should move from:

- compact executive context
- to concentrated operational pressure
- to direct action cues
- to client-level follow-up context

## Current Working Page Structure

Recommended page order:

1. `Top KPIs`
2. `Visao Operacional`
3. `Fila de Prioridades`
4. `Carteira em Foco`
5. `Cliente 360 / Drilldown`
6. `Apoio / Detalhes`

### Why this structure

- `Top KPIs` answer: how is the carteira overall?
- `Visao Operacional` answers: where is pressure concentrated?
- `Fila de Prioridades` answers: what needs action now?
- `Carteira em Foco` answers: which accounts deserve attention first?
- `Cliente 360 / Drilldown` answers: what context is needed before acting?
- `Apoio / Detalhes` holds useful but non-primary inspection context

### Current central section decision

If one section becomes the working center of the page, it should be
`Fila de Prioridades`.

Rationale:

- it converts flags into visible work
- it supports business resolution more directly than isolated cards
- it better matches the goal of an action-oriented dashboard

### Current working intent for `Fila de Prioridades`

Suggested columns:

- Prioridade
- Flag principal
- Cliente
- Pedido / Seq
- Material
- Qtd faltante
- Valor / peso relevante
- Prazo
- Motivo
- Acao sugerida

Suggested sort logic:

- severity and delivery proximity first
- then commercial weight
- then client relevance

This section is the strongest candidate to absorb most of the visibility
currently split across:

- `Bloqueio de Credito`
- `Entrega em Atencao`
- `Cliente de Alto Valor`
- `Clientes com Flags`

## Resume Point For Next Session

The next dashboard discussion should start here:

1. refine the exact contents and ordering logic of `Fila de Prioridades`
2. refine the next `Visao Operacional` insights
3. decide what belongs in `Carteira em Foco` versus `Cliente 360`
4. decide which supporting sections belong under `Apoio / Detalhes`

Recommended opening prompt for continuation:

`Resume SRP-13 dashboard discussion from the working notes file and continue with Fila de Prioridades and the next dashboard sections.`
