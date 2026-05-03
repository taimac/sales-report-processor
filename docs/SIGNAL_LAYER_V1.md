# Signal Layer V1 — Intelligence Detection Design
### Systems Domain | Sales Report Processor
**Created:** 2026-05-02  
**Updated:** 2026-05-03  
**Layer:** 2 — Action Signals (within the three-layer intelligence architecture)  
**Status:** Conceptual design — schema-level definitions, no private data

---

## Purpose

This document defines the first version of the signal layer: what the system detects from processed operational data, what each signal means to the business, and what it should trigger.

Signals are the bridge between Layer 1 (Data Intelligence — what is happening) and Layer 3 (Organizational Intelligence — how to act correctly). They transform structured data into prioritized, human-readable business alerts.

**Privacy note:** All definitions here are schema-level and conceptual. No client names, prices, or private operational records are included or implied. The trigger conditions describe data patterns, not actual data.

---

## Architecture Position

```
Raw Reports (TXT, PDF)
        ↓
Layer 1: Data Intelligence
(parse → structure → normalize)
        ↓
Layer 2: Action Signals  ← this document
(detect patterns → classify → prioritize)
        ↓
Layer 3: Organizational Intelligence
(surface playbook → knowledge → training)
        ↓
User sees: situation + recommended action + how to act
```

---

## Signal Design Principles

- Each signal must answer a real business question, not just report a number
- Severity classifies urgency, not importance — all signals matter, some are time-critical
- Every signal should connect to at least one playbook entry in Layer 3
- Signals should be actionable: the user must be able to do something specific after seeing it
- Avoid alert fatigue: signals fire when conditions are genuinely abnormal, not as routine reporting

---

## Current SRP Source Fields

SRP already parses enough fields to support the first operational signals without adding a new data source.

- `ParsedReport`: `generated_date`, `generated_time`
- `CustomerSection`: `representative`, `customer_name`
- `ParsedItem`: `pedido`, `seq`, `descricao`, `ord_prod`, `sit_ordem`, `dt_entr`, `qt_ped`, `qt_pc`, `qt_prod`, `qt_fatur`, `sdo_estoq`, `sit`, `pre_liq`, `transp`, `cr_pro`, `cr_fat`, `o_compra`, `item_cli`
- `CustomerTotal`: `total_ped`, `total_in_prod`, `total_fatur`, `total_sdo`, `total_valor`
- `ReportTotal`: `total_ped`, `total_in_prod`, `total_fatur`, `total_sdo`, `total_valor`

The current dashboard service already computes first-pass operational buckets:

| Current bucket | Meaning | Can feed |
|---|---|---|
| `delivery_attention` | Delivery date is near, overdue, or missing while open balance exists | S1, S4 |
| `credit_block` | Production or billing credit status is blocked | S2 |
| `production_follow_up` | Produced quantity/status exists but invoicing or follow-up is incomplete | S1, S4, S6 |
| `missing_production_reference` | Commercial order exists without production reference | S4, S6 |
| `stock_balance` | Open balance exists on the item | S1, S5 |
| `high_value_customer` | Customer is among the highest open-value/open-quantity rows | S1, S7 |

This means V1 does not need to invent signals from scratch. It should formalize and stabilize the commercial meaning of the signals already emerging from the dashboard work.

---

## Signal Definitions

---

### S1 — Delayed High-Value Orders

**Business meaning:**  
One or more high-value orders have passed their expected delivery or fulfillment date without confirmation or resolution. Financial exposure is accumulating and client trust is at risk.

**Trigger condition:**  
Order status is not confirmed/delivered AND current date exceeds expected date AND order value is above defined threshold.

**Current SRP source fields:**  
`dt_entr`, `sdo_estoq`, `qt_ped`, `qt_prod`, `qt_fatur`, `pre_liq`, `pedido`, `seq`, `customer_name`, `total_valor`, dashboard buckets `delivery_attention`, `stock_balance`, `high_value_customer`.

**Severity:** High  
**Time sensitivity:** Immediate — each day of delay compounds risk

**Recommended action:**  
Contact supplier for status update. If no response within defined window, escalate. Log outcome.

**Layer 3 connection:**  
→ Delayed order playbook  
→ Supplier escalation script  
→ Client communication template (how to proactively inform client without creating panic)

---

### S2 — Payment Exposure Spike

**Business meaning:**  
The cumulative value of overdue or unconfirmed payments from one or more clients has crossed a risk threshold. The business has significant financial exposure that requires active management.

**Trigger condition:**  
Sum of outstanding receivables for a client (or total portfolio) exceeds defined threshold AND days overdue exceeds defined minimum.

**Current SRP source fields:**  
`cr_pro`, `cr_fat`, `customer_name`, `pedido`, `seq`, `total_valor`, dashboard bucket `credit_block`.

**Current limitation:**  
SRP can already detect credit blocks from report fields. True receivables aging requires either richer report fields or integration with financial data.

**Severity:** High  
**Time sensitivity:** Urgent — exposure compounds daily

**Recommended action:**  
Prioritize contact with highest-exposure clients. Review credit terms. Flag for management visibility.

**Layer 3 connection:**  
→ Collections conversation playbook  
→ Payment renegotiation script  
→ Decision rule: when to pause new orders for a client with exposure above X

---

### S3 — Client Silence Risk

**Business meaning:**  
A previously active client has gone quiet — no recent orders, no communications, no activity — for longer than their typical engagement pattern. This often precedes churn or signals a problem the client hasn't raised.

**Trigger condition:**  
Client was active (had orders or interactions) within the past N months AND has had zero activity for M weeks, where M is above that client's typical interval.

**Current SRP source fields:**  
Not fully available from a single report. Requires historical snapshots across `ParsedReport` plus `CustomerSection.customer_name` and customer/order presence over time.

**Current limitation:**  
This is a V1.5 signal unless SRP keeps enough historical parsed reports to compare customer activity across periods.

**Severity:** Medium  
**Time sensitivity:** Not immediate, but window closes — the longer the silence, the harder the recovery

**Recommended action:**  
Proactive outreach. Not a collection call — a relationship call. Check in, understand their current situation, surface any unspoken issues.

**Layer 3 connection:**  
→ Re-engagement call script  
→ Lessons learned: what re-engagement approaches have worked for this client type  
→ Training note: how to distinguish temporary slowdown from early churn signal

---

### S4 — Production Bottleneck

**Business meaning:**  
A supplier's backlog or response pattern suggests production capacity issues. Orders may not arrive on time even if confirmed, creating downstream risk for client commitments.

**Trigger condition:**  
Average response time or fulfillment rate for a supplier has degraded beyond normal variance AND multiple open orders are affected.

**Current SRP source fields:**  
`ord_prod`, `sit_ordem`, `sit`, `dt_entr`, `qt_prod`, `qt_fatur`, `sdo_estoq`, `transp`, dashboard buckets `production_follow_up`, `missing_production_reference`, `delivery_attention`.

**Current limitation:**  
The current public SRP repo does not model supplier identity as a first-class field. V1 can still flag production bottleneck patterns inside the report, but supplier-level scoring belongs later.

**Severity:** Medium-High (escalates with volume at risk)  
**Time sensitivity:** Requires early action — bottlenecks worsen if not managed proactively

**Recommended action:**  
Alert clients proactively. Evaluate alternative suppliers for critical items. Adjust order timing.

**Layer 3 connection:**  
→ Proactive client communication playbook (how to frame a delay before the client asks)  
→ Alternative supplier assessment checklist  
→ Decision rule: threshold for switching suppliers vs. waiting

---

### S5 — Stock Anomaly

**Business meaning:**  
Inventory levels for key items show unexpected depletion, accumulation, or inconsistency relative to expected patterns. This may indicate an input error, an unlogged transaction, or a genuine supply/demand mismatch.

**Trigger condition:**  
Reported stock level deviates from expected level (based on recent transactions) beyond a defined variance threshold.

**Current SRP source fields:**  
`sdo_estoq`, `qt_ped`, `qt_pc`, `qt_prod`, `qt_fatur`, `sit`, `sit_ordem`, dashboard bucket `stock_balance`.

**Current limitation:**  
Single-report SRP can identify open stock/balance requiring attention. True anomaly detection needs either historical comparison or an expected-stock rule.

**Severity:** Medium  
**Time sensitivity:** Moderate — investigate before the discrepancy compounds or causes a client commitment failure

**Recommended action:**  
Verify physical count. Reconcile with transaction history. If confirmed anomaly, investigate cause before taking commercial action.

**Layer 3 connection:**  
→ Stock reconciliation procedure  
→ Training note: common causes of anomalies and how to distinguish data error from real discrepancy

---

### S6 — Priority Follow-Up Overdue

**Business meaning:**  
One or more clients or orders have been flagged for follow-up but no action has been logged within the expected window. The commitment to act is present but the action hasn't happened.

**Trigger condition:**  
Follow-up flag exists AND no action log entry has been recorded AND time since flag exceeds defined window.

**Current SRP source fields:**  
All current dashboard buckets can create follow-up candidates. Completion status is not yet modeled.

**Current limitation:**  
This becomes implementable when SRP or SalesApp stores action logs, explicit deferrals, and follow-up timestamps.

**Severity:** Medium  
**Time sensitivity:** Moderate — depends on what was flagged, but unfollowed commitments erode trust

**Recommended action:**  
Review the flagged items. Complete or explicitly defer the follow-up with a logged reason.

**Layer 3 connection:**  
→ Follow-up discipline playbook  
→ Training note: why follow-up logging matters (institutional memory, not just accountability)

---

### S7 — Opportunity Window

**Business meaning:**  
A client with a strong historical purchase pattern has been inactive longer than typical. Unlike S3 (Silence Risk, which is about churn), this signal identifies a buying cycle opportunity — the client may be ready to order again.

**Trigger condition:**  
Client has a defined purchase frequency pattern AND time since last order is within or slightly past that frequency window AND client has no open disputes or payment issues.

**Current SRP source fields:**  
`CustomerSection.customer_name`, `CustomerTotal.total_valor`, `total_sdo`, repeated `ParsedReport` snapshots over time, dashboard bucket `high_value_customer`.

**Current limitation:**  
Requires historical customer activity. It should not be implemented from one uploaded report alone.

**Severity:** Low (opportunity, not risk)  
**Time sensitivity:** Moderate — opportunity windows close if a competitor moves first

**Recommended action:**  
Proactive commercial outreach. Lead with value, not a sales push. Offer relevant information (new products, price updates, market conditions relevant to them).

**Layer 3 connection:**  
→ Opportunity outreach script  
→ Lessons learned: what approaches have historically converted this pattern into orders

---

## Signal Summary Table

| ID | Name | Severity | Time Sensitivity | Layer 3 Connection |
|----|------|----------|------------------|--------------------|
| S1 | Delayed High-Value Orders | High | Immediate | Delayed order playbook, supplier escalation, client communication |
| S2 | Payment Exposure Spike | High | Urgent | Collections playbook, renegotiation script, credit decision rule |
| S3 | Client Silence Risk | Medium | Window closes | Re-engagement script, churn distinction training |
| S4 | Production Bottleneck | Medium-High | Early action needed | Proactive client communication, alternative supplier checklist |
| S5 | Stock Anomaly | Medium | Investigate promptly | Reconciliation procedure, anomaly diagnosis training |
| S6 | Priority Follow-Up Overdue | Medium | Moderate | Follow-up discipline playbook |
| S7 | Opportunity Window | Low | Moderate | Opportunity outreach script, historical conversion lessons |

---

## Next Steps for This Layer

- Split the signals into immediate and later implementation groups:
  - Immediate from current SRP fields: S1, S2 credit-block subset, S4 report-level subset, S5 basic stock-balance subset
  - Later with history/action logging: S3, S6, S7, full S2 receivables aging
- Define threshold values for each immediate trigger condition (requires operational data review — done in private implementation context)
- Build corresponding Layer 3 entries for each signal (see `KNOWLEDGE_ACTION_LAYER.md` in `/shared/`)
- Sequence for implementation: S1 and S2 first (highest business impact), S3 and S7 second (relationship layer), S4-S6 third (operational refinement)
