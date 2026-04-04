# AI Output Contracts – SRP

## Purpose

Define standard output formats for SRP work.

Outputs must be:
- clear
- structured
- scoped
- actionable

---

## Core Rule

Choose the smallest contract that fits the task.

Do not over-structure simple answers.

---

## Global Rules

- Stay within MVP scope
- Prefer implementation-ready output
- Keep wording concise
- Avoid unnecessary theory
- Include validation steps when relevant

---

## Contract 1 – Analysis Output

### Use for
reviews, gap analysis, planning

### Format

# Analysis

## Scope
- Topic:
- Relevant area:
- Relevant files:

## Findings
- [finding]

## Risks / Gaps
- [risk]

## Recommendation
- [next step]

## Contract 2 – Jira Story Output

### Use for
story creation or refinement

### Format

# Jira Story: SRP-XXX – [Title]

## Description
[clear description]

## Goal
[what success looks like]

## Scope

### Included
- [item]

### Not Included
- [item]

## Acceptance Criteria
- [ ] [criterion]

## Technical Notes
- [note]

## Dependencies
- [dependency]

## Suggested Story Points
- [number]

## Contract 3 – Jira Subtask Output

### Use for
technical task breakdown

### Format

# Jira Subtask: SRP-XXX – [Title]

## Parent Story
- SRP-XXX – [Parent title]

## Purpose
[why this exists]

## Scope
- [item]

## Deliverables
- [deliverable]

## Acceptance Criteria
- [ ] [criterion]

## Technical Notes
- Files:
- API impact:
- Validation notes:

## Suggested Story Points
- [number]

## Contract 4 – Backend Implementation Output

### Use for
models, views, serializers, services, endpoints

### Format

# Backend Implementation

## Objective
[what is being implemented]

## Scope
- Ticket:
- App:
- Files:

## Implementation Notes
- [note]

## Code

```python
code here
```

## Validation

```
command here
```

## Success Criteria
[success path]

## Failure Cases
[failure path]

## Contract 5 – Documentation Output

### Use for
README sections, architecture notes, setup docs

### Format

# Documentation

## Purpose
[what this document is for]

## Scope
- [area]

## Content
[final markdown-ready content]