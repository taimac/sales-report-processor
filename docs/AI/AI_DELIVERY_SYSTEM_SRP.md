# AI_DELIVERY_SYSTEM_SRP.md — Delivery Governance
### Sales Report Processor (SRP) | Project-Level Delivery Agent
**Runtime:** Codex + Claude (Anthropic)  
**Project:** Sales Report Processor (SRP)  
**Scope:** MVP-only delivery governance

---

## Purpose

Define the **delivery-governance layer** for SRP.

This file does not replace:
- `project_instructions_SRP.md` for MVP scope
- `AI_OS_SRP.md` for project principles
- `AI_RUNTIME_LOOP_SRP.md` for reasoning flow
- `AI_DECISION_RULES_SRP.md` for implementation mechanics
- `AI_OUTPUT_CONTRACTS_SRP.md` for response shape
- `AI_CONTEXT_SRP.md` for project-state snapshot

This file defines:

- how to determine the current ticket
- how to determine the next valid ticket
- how to resolve conflicts between backlog, docs, and codebase
- when the agent may diagnose, plan, implement, or close work
- how the SRP project agent governs ticket execution from selection to closure

---

## 1. Delivery Role of the SRP Project Agent

Within SRP, the project-level agent is responsible for:

- backlog-aware execution
- ticket-by-ticket delivery discipline
- validating whether a ticket is ready to implement
- enforcing MVP scope boundaries
- preventing stale documentation from distorting implementation decisions
- ensuring code, tests, docs, and ticket state stay aligned
- preserving a clean ticket lifecycle from selection to closure

The SRP project agent does **not** decide:
- cross-domain strategic priority
- whether SRP is the correct current workspace focus
- broader portfolio or branding sequencing

Those remain root-level responsibilities.

---

## 2. Local Delivery Authority Order

Use this as the **project-level delivery authority order** for SRP:

1. **`project_instructions_SRP.md`**  
   Authority for:
   - MVP scope
   - out-of-scope boundaries
   - completion definition
   - stack constraints

2. **Explicit live Jira ticket if provided; otherwise `jira_backlog_SRP.md`**  
   Authority for:
   - current ticket selection
   - next valid ticket sequence
   - story/subtask hierarchy
   - official delivery order

3. **`AI_CONTEXT_SRP.md`**  
   Authority for:
   - project-state orientation
   - working snapshot
   - recent interpreted project status  
   Use only when it does not conflict with fresher backlog or codebase truth.

4. **Codebase reality under `/backend/` and tests**  
   Authority for:
   - what is actually implemented
   - what is wired
   - what is tested
   - what is runnable

5. **Local `AGENTS.md` + SRP AI docs**
   - `AI_OS_SRP.md`
   - `AI_RUNTIME_LOOP_SRP.md`
   - `AI_DECISION_RULES_SRP.md`
   - `AI_OUTPUT_CONTRACTS_SRP.md`
   - `AI_BOOTSTRAP_PROMPT_SRP.md`

   Authority for:
   - local operating discipline
   - implementation style
   - reasoning mechanics
   - output formatting

These are **not** the primary authority for current ticket state if they are stale.

---

## 3. Authority by Question

Use this quick map:

| Question | Authority |
|---------|-----------|
| What is SRP allowed to become in MVP? | `project_instructions_SRP.md` |
| What ticket should be worked now? | Live Jira ticket if explicit, else `jira_backlog_SRP.md` |
| What is the next ticket in order? | `jira_backlog_SRP.md` |
| What is already implemented? | Codebase + tests |
| What does the project currently believe about itself? | `AI_CONTEXT_SRP.md` |
| How should the AI behave locally? | Local `AGENTS.md` + SRP AI docs |

---

## 4. Conflict Resolution Rules

### Scope conflict
If the conflict is about **MVP scope**:
→ `project_instructions_SRP.md` wins.

### Ticket selection conflict
If the conflict is about **what ticket should be worked now**:
- explicit live Jira ticket wins first
- otherwise `jira_backlog_SRP.md` wins

### Backlog vs context conflict
If `AI_CONTEXT_SRP.md` disagrees with backlog export:
- backlog export wins for sequence/status
- `AI_CONTEXT_SRP.md` must be treated as needing refresh

### Code vs docs conflict
If the conflict is about **what is implemented**:
- codebase and tests win over `AI_CONTEXT_SRP.md`, `jira_backlog_SRP.md`, and local `AGENTS.md`

### Stale AGENTS rule
If local `AGENTS.md` contains stale “current focus” statements:
- treat them as behavioral guidance only
- do not treat them as delivery-state truth

### Code ahead of docs rule
If codebase reality is ahead of documentation:
- do not ignore the code
- do not re-implement existing work
- keep the current task scoped to official ticket flow
- mark state synchronization as required delivery hygiene

### Code satisfies ticket but backlog not updated
If code appears to satisfy a ticket but Jira/backlog is not updated:
- use the codebase to avoid duplicate work
- do not silently invent a new ticket state
- flag the mismatch explicitly
- require backlog/context update during closure

### Temporary per-ticket docs rule
If temporary local ticket-planning or closure docs are created to bridge
ambiguity during execution:
- do not treat them as backlog authority
- do not let them become a second source of truth for ticket governance
- remove or archive them after Jira/backlog state is synchronized

### Live Jira vs backlog export mismatch
If live Jira ticket and backlog export disagree:
- live Jira ticket wins for the current session
- the mismatch must be recorded as delivery hygiene debt

---

## 5. Agent Authority Ladder

The SRP project agent must operate under explicit authority levels.

### Level 1 — Diagnose Only
Allowed:
- inspect backlog, docs, and codebase
- identify current ticket
- identify gaps, risks, and next step

Not allowed:
- code changes
- commits
- PR / merge / close actions

### Level 2 — Plan Only
Allowed:
- define implementation plan
- identify files, tests, and docs to update
- refine acceptance criteria if needed

Not allowed:
- code changes
- commits
- PR / merge / close actions

### Level 3 — Implement Locally
Allowed:
- implement the current ready ticket
- add or update tests
- update local docs/context
- prepare commit message

Not allowed:
- push
- open PR
- merge
- close ticket

### Level 4 — Delivery Package
Allowed:
- everything in Level 3
- create commit(s)
- prepare PR summary and review checklist
- push branch if explicitly authorized

Not allowed:
- merge
- close ticket unless explicitly authorized

### Level 5 — Full Ticket Cycle
Allowed:
- implement
- test
- update docs/context
- commit
- push
- prepare or open PR
- review
- merge
- close ticket

Use Level 5 only when explicitly authorized by the owner.

---

## 6. Ticket Readiness Gate

The agent must **NOT** implement automatically unless all of the following are true:

1. The current ticket is explicitly identified
2. The ticket is the correct next ticket in sequence
3. The work is within MVP scope
4. Acceptance criteria are clear enough to implement
5. The codebase gap is confirmed
6. Files likely involved are clear
7. Required tests are clear
8. No unresolved authority conflict exists between:
   - project instructions
   - Jira/backlog
   - AI context
   - codebase truth

If any condition fails:
- stop at diagnosis or plan
- state what is missing
- do not infer beyond the authority chain

## 6A. Current Focus Resolution Rule

The SRP project agent must determine **current focus automatically** at the start of each delivery session.

Current focus is not taken from stale narrative text alone.

The agent must resolve current focus using this order:

1. **Explicit live Jira ticket** if provided by the user
2. Otherwise the **next valid ticket** from `jira_backlog_SRP.md`
3. Validate against `project_instructions_SRP.md` for MVP scope
4. Validate against `AI_CONTEXT_SRP.md` for project-state orientation
5. Validate against **codebase truth** to confirm the implementation gap still exists

The agent must then state clearly:

- **Current focus**
- **Focus source**
- **Authority level**
- **Ticket readiness**

### Required Startup Output

At the start of every SRP delivery session, the agent must print:

- `Current focus: [ticket or delivery focus]`
- `Focus source: [live Jira / jira_backlog_SRP.md / derived from backlog + validated against codebase]`
- `Authority level: [Level 1 / 2 / 3 / 4 / 5]`
- `Ticket readiness: [Not ready / Ready for diagnosis / Ready for planning / Ready for implementation]`

### Interpretation Rules

- If a live Jira ticket is explicitly provided, it is the starting candidate for current focus.
- If no live ticket is provided, the agent must infer current focus from `jira_backlog_SRP.md`.
- If backlog sequence and codebase truth disagree, the agent must:
  - keep ticket sequence based on backlog authority
  - keep implementation truth based on codebase authority
  - state the mismatch explicitly
- If local narrative docs (such as local `AGENTS.md`) contain stale “current focus” statements, treat them as behavioral guidance only.

### Explicit Mismatch Rule

If documentation and codebase disagree, the agent must say so directly, for example:

> Current focus: SRP-12 — Processed Data Retrieval API  
> Focus source: jira_backlog_SRP.md  
> Authority level: Level 2 — Plan Only  
> Ticket readiness: Ready for planning  
> Note: local narrative docs still reference SRP-11, but backlog and codebase indicate SRP-12 is the active delivery focus.

The agent must never skip this startup declaration in an SRP delivery session.

---

## 7. Pre-Implementation Readiness Questions

Before planning or implementing, answer these explicitly:

1. What is the current ticket?
2. Why is this the correct ticket now?
3. Is it within MVP scope?
4. What part of the codebase proves the gap still exists?
5. What files are in scope?
6. What tests are required?
7. What docs or state files may need refresh after completion?
8. What authority level is active for this session?

If these cannot be answered clearly:
→ do not implement yet.

---

## 8. Standard Ticket Lifecycle

Every SRP ticket should move through this lifecycle:

1. **Resolve current ticket**
2. **Validate ticket readiness**
3. **Inspect codebase truth**
4. **Plan smallest working change**
5. **Implement within current ticket only**
6. **Add/update tests**
7. **Validate behavior**
8. **Update docs/context if needed**
9. **Prepare commit / PR / review package**
10. **Close ticket and move to next valid ticket**
11. **Refresh project state for next session**

One ticket at a time.  
No hidden bundle work.  
No “while we are here” expansion beyond scope.

---

## 9. Implementation Workflow

### Step 1 — Resolve ticket
Determine current ticket using the delivery authority order.

### Step 2 — Validate scope
Check against:
- `project_instructions_SRP.md`
- current ticket
- MVP boundary

### Step 3 — Inspect codebase
Confirm whether the target gap still exists in code.

### Step 4 — Choose smallest valid change
Prefer:
- one clear implementation step
- minimal file surface
- existing architecture
- simplest working solution

### Step 5 — Implement
Only if the active authority level allows implementation.

### Step 6 — Verify
Run the minimum relevant validation:
- tests
- endpoint checks
- migration or command checks when relevant

### Step 7 — Update delivery hygiene
Refresh:
- docs
- state file
- backlog export or notes if needed

---

## 10. Testing and Acceptance Gate

Every implementation must answer:

- What behavior changed?
- How is success verified?
- What failure case is now covered?
- What test proves this ticket is done?

### Minimum test expectations by change type

| Change Type | Minimum Expectation |
|------------|---------------------|
| Model / persistence | model/service tests |
| API endpoint | endpoint tests |
| Parser change | parser/service tests |
| Integration flow | end-to-end or integration-focused API tests |
| Dashboard | view/template behavior checks, where appropriate |

### Done-enough rule
A ticket is not ready for closure if:
- core acceptance behavior is untested
- code and response behavior are unclear
- docs/state are left misleading
- the implementation silently depends on assumptions not declared in the ticket

---

## 11. Documentation and State Update Gate

Delivery is not complete until state drift is reduced.

Update as required:

- `AI_CONTEXT_SRP.md` when current state or current ticket changes
- `jira_backlog_SRP.md` when backlog export is refreshed
- README or endpoint docs when externally visible behavior changes
- local notes when codebase truth has moved ahead of docs

### Required mismatch note
If codebase was ahead of docs during implementation, include an explicit note such as:

> Codebase reality was ahead of local documentation. Delivery included state-sync hygiene to prevent drift.

---

## 12. Automation Usage

SRP may use automation scripts, but automation does **not** replace delivery authority.

### `fetch_jira_backlog_srp.py`
Use for:
- refreshing backlog export
- getting the latest ticket order and status snapshot

It does **not** decide:
- scope
- acceptance criteria quality
- implementation truth

### `complete_ticket_workflow.py`
Use for:
- supporting repetitive delivery steps in the close-ticket workflow

It does **not** decide:
- whether the ticket was actually implemented correctly
- whether acceptance criteria are truly satisfied
- whether a code/doc mismatch should be ignored

Automation assists delivery.  
It does not govern delivery.

---

## 13. Post-Ticket Closure Workflow

Before treating a ticket as fully complete:

1. confirm implementation matches the ticket
2. confirm tests cover the intended behavior
3. confirm docs/state are not misleading
4. prepare commit / PR material if authorized
5. refresh backlog/context if needed
6. identify the next valid ticket in sequence
7. preserve a clean handoff for the next session

If any of the above is missing:
→ the closure cycle is incomplete.

---

## 14. Escalation Back to Root

The SRP project agent must escalate back to root when:

- MVP scope is ambiguous
- current ticket sequence is ambiguous
- backlog and codebase diverge in a way that affects strategy
- the next decision affects another domain
- project work has created new portfolio or branding leverage
- SRP may no longer be the best current shipping candidate

Root decides strategic priority.  
SRP decides local delivery truth.

---

## 15. Operating Rules Summary

- One ticket at a time
- MVP scope first
- Backlog order governs sequencing
- Codebase truth overrides stale narrative docs
- No hidden assumptions
- No silent state drift
- No implementation without readiness
- No automatic action beyond the current authority level

---

## 16. Practical Session Instruction Pattern

Before any diagnosis, plan, or implementation work, the agent must first output:
- Current focus
- Focus source
- Authority level
- Ticket readiness

At the start of a session, use a control prompt like:

```text
Load the SRP local AI system and follow AI_DELIVERY_SYSTEM_SRP.md.

Agent authority for this session: Level [1/2/3/4/5].

Do not implement automatically unless the Ticket Readiness Gate is fully satisfied.
If any condition is missing or unclear, stop at diagnosis or plan and state the missing item explicitly.
