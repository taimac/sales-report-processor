# AI Output Contracts – SRP

## Purpose

Standard output formats for SRP work.

Outputs must be: clear, structured, scoped, actionable.

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

## Contract 1 – Review Output

### Use for
Gap analysis, code reviews, planning sessions.

### Format

```
# Review

## Scope
- Topic:
- Relevant files:

## Findings
- [finding]

## Risks / Gaps
- [risk]

## Recommendation
- [next step]
```

---

## Contract 2 – Jira Story Output

### Use for
Story creation or refinement.

### Format

```
# Jira Story: SRP-XXX – [Title]

## Description
[clear description of what this story delivers]

## Goal
[what success looks like — one sentence]

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
- SRP-XXX must be Done before this starts
- [or: No dependencies]

## Suggested Story Points
- [number]
```

---

## Contract 3 – Jira Subtask Output

### Use for
Technical task breakdown within a story.

### Format

```
# Jira Subtask: SRP-XXX – [Title]

## Parent Story
- SRP-XXX – [Parent title]

## Purpose
[one sentence: why this subtask exists]

## Scope
- [item]

## Deliverables
- [file or artifact produced]

## Acceptance Criteria
- [ ] [criterion]

## Technical Notes
- Files: [e.g. reports/models.py]
- API impact: [e.g. none / adds POST /api/reports/upload/]
- Validation notes: [e.g. must reject files over 10MB]

## Dependencies
- SRP-XXX must be Done
- [or: No dependencies]

## Suggested Story Points
- [number]
```

---

## Contract 4 – Backend Implementation Output

### Use for
Models, views, serializers, services, parsers, endpoints.

### Format

```
# Backend Implementation

## Objective
[what is being implemented — one sentence]

## Scope
- Ticket: SRP-XXX
- App: reports
- Files:
  - reports/models.py
  - reports/serializers.py

## Implementation Notes
- [note]

## Code

[filename]
```python
# code here
```

## Validation

```bash
# command to verify it works
python manage.py migrate
python manage.py test reports
```

## Success Criteria
[what the happy path looks like]

## Failure Cases
- Invalid file type → returns 400 with message "Unsupported file type"
- File missing → returns 400 with message "No file provided"
- Parse error → returns 422 with message "Could not extract data from file"
```

---

## Contract 5 – Documentation Output

### Use for
README sections, setup docs, architecture notes.

### Format

```
# Documentation

## Purpose
[what this document is for]

## Scope
- [area]

## Content
[final markdown-ready content]
```
