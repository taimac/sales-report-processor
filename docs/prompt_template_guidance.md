# Prompt Template Guidance (SRP)

## 1. Base Template (default)

```text
You are working on the Sales Report Processor (SRP).

Follow strictly AGENTS.md.

Current ticket:
[SRP-XXX – Title]

Context:
- Parser is complete
- Working inside backend/reports/
- MVP scope only

Task:
Generate Backend Implementation output.

Constraints:
- Stay strictly within ticket scope
- Do not add extra features
- Keep solution minimal and runnable
```

---

## 2. Planning (subtasks)

```text
Follow AGENTS.md.

Current ticket:
[SRP-XXX – Title]

Task:
Generate Jira Subtasks.

Constraints:
- Keep tasks small and executable
- Respect MVP scope
```

---

## 3. Review (after coding)

```text
Follow AGENTS.md.

Task:
Review this implementation against:
- Current ticket: [SRP-XXX]
- MVP scope

Focus:
- Scope violations
- Over-engineering
- Missing requirements
```

---

## 4. Fix / Correction

```text
This is outside ticket scope.

Regenerate following:
- AGENTS.md
- Current ticket: [SRP-XXX]
- MVP constraints only
```

---

## 5. Force Implementation Output

```text
Regenerate using Backend Implementation contract only.
No explanations.
```

---

## 6. Debug / Issue

```text
Follow AGENTS.md.

Problem:
[describe error]

Context:
[relevant code or behavior]

Task:
Provide minimal fix within current ticket scope.
```

---

## 7. Golden Rules (remember)

* Always include **ticket**
* One prompt = one task
* Prefer **“generate implementation”** over asking questions
* Reject anything outside scope
* Keep everything **simple + runnable**

---

This is your **daily operating cheat sheet**.
