---
title: SimpleSpan Plan Schema Specification
version: 1.0
context: ai/automation/schema
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# 📐 SimpleSpan Plan Schema (v1.0)

This document defines a **portable, minimal schema** for any roadmap/plan that AI agents (AIC, Planner, Implementer) can use across domains and repositories.

---

## 1. Purpose & Non-Goals
**Purpose:** Standardize the structure of planning documents so tools like `aic_orchestrator.py` can parse _current phase_, _checklists_, and _CCP_ information reliably.  
**Non-Goals:** This schema does **not** prescribe domain content (e.g., FEA vs Section Properties). It only defines format.

---

## 2. Front-Matter Specification
Every plan **must** start with YAML front-matter:

```yaml
---
title: <string>              # Human-readable title
version: <string|int>        # e.g., 1.0 or 1
context: <string>            # domain or area (e.g., 'fea/moving-loads', 'sections/properties')
schema_version: 1            # Plan schema version (start at 1)
last_reviewed: <YYYY-MM-DD>  # ISO date
ai_context: true             # must be true
---
```

**Validation Rules**
- `schema_version` must equal a supported schema (current: `1`).
- `ai_context` must be `true`.

---

## 3. Resume Context Block
A fenced code block labeled `yaml` that includes `resume_context`:

```yaml
resume_context:
  current_phase: <int>       # Required
  last_ccp: <string>         # Required (can be '—' if none yet)
  progress_file: <path>      # Required, e.g., 'reports/progress.md'
  key_docs:                  # Optional
    - <path>
    - <path>
```

**Rules**
- Exactly **one** `resume_context` block per plan.
- `current_phase` is an integer in range `[0..N]` where `N` is the highest phase in the file.

---

## 4. Phase Sections
Each phase must follow this pattern:

```markdown
## Phase N — Title
(optional description)

### ✅ Checklist
- [ ] Task A
- [x] Task B

### Deliverables
- (optional bullets)

### Acceptance Criteria
- (optional bullets)
```

**Selectors used by tools (regex):**
- Phase header: `^##\s+Phase\s+(\d+)\s+[—-]\s+(.*)$`
- Checklist header: `^###\s+✅\s+Checklist\s*$`
- Items: `^\s*-\s*\[(x| )\]\s+(.*)$`

**Rules**
- At least **one** phase must be present.
- Each phase must contain a `### ✅ Checklist` section with ≥1 item.
- Nested checklists are **not** allowed (flat list only).

---

## 5. CCP Guidance (Continuity Checkpoints)
- Create a CCP when all acceptance criteria for a phase are met.
- Suggested naming: `<prefix>-<phase>-<slug>` (e.g., `vSEC-1-ccp-schema`).
- CCPs are recorded in `reports/progress.md` and (optionally) an ADR.

---

## 6. Validation
A plan is **valid** if:
- Front-matter satisfies §2.
- Exactly one `resume_context` exists (§3).
- Phases and checklists follow §4.
- Contains ≥1 phase.

**Common Failures**
- Missing `resume_context`
- Using `### Checklist` without the ✅ marker (must be `### ✅ Checklist`)
- Using `* [ ]` instead of `- [ ]`

---

## 7. Versioning & Backward Compatibility
- Increment `schema_version` only when breaking changes to structure occur.
- Tools must support `N` and `N-1` versions for a 1 minor-version grace period.

---

## 8. Examples

### ✅ Minimal Valid Example
```markdown
---
title: Example Portable Plan
version: 1.0
context: sections/properties
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

## 🧭 YAML Resume Context

```yaml
resume_context:
  current_phase: 1
  last_ccp: vEX-0-ccp-baseline
  progress_file: reports/progress.md
```

## Phase 0 — Baseline
### ✅ Checklist
- [x] Initialize repo structure
- [x] Add progress.md

## Phase 1 — Spec
### ✅ Checklist
- [ ] Draft spec
- [ ] Validate schema
```

### ❌ Invalid Example (no resume_context)
```markdown
---
title: Bad Plan
version: 1
context: demo
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

## Phase 1 — Missing Resume
### ✅ Checklist
- [ ] Do a thing
```
