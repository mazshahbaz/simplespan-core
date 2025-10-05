---
title: AI Session Logging Schema
version: 1.0
context: ai/automation/schema
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# AI Session Logging Schema v1.0

## Purpose
Define the structure for logging all AI-assisted work sessions to ensure traceability, auditability, and compliance with SimpleSpan governance.

## Log Format
AI sessions are logged in YAML format in `reports/progress.md` and optionally in detailed session files.

---

## Session Entry Structure

### Progress Log Entry (Required)
Each AI session must add one line to `reports/progress.md`:

```
YYYY-MM-DD | <Actor> | Phase <N> | <Plan> | <Summary> | <CCP or —> | <Link or —>
```

**Fields:**
- **Date**: ISO format YYYY-MM-DD
- **Actor**: `Human`, `Claude Code`, `GPT-5 (AIC)`, `Cursor`, etc.
- **Phase**: Current phase number from active plan
- **Plan**: Short reference to plan file (e.g., `v5.0`, `AIC roadmap`)
- **Summary**: One-line description of work completed (≤100 chars)
- **CCP**: Continuity checkpoint tag or `—` if none
- **Link**: PR number, issue number, or `—` if none

### Detailed Session Log (Optional)
For complex sessions, create detailed log in `reports/ai/sessions/YYYY-MM-DD-<slug>.yaml`:

```yaml
---
session_id: YYYY-MM-DD-<slug>
date: YYYY-MM-DD
time_start: HH:MM:SS
time_end: HH:MM:SS
actor: <AI_agent_name>
agent_type: planner|implementer|reviewer|auditor
plan_reference: <path_to_plan>
phase: <integer>

context_loaded:
  - <path1>
  - <path2>
  - <path3>

intent:
  goal: <human_intent_description>
  type: plan|module|feature|refactor|fix
  scope: <module_or_area>

actions:
  - action: <create|edit|delete>
    file: <file_path>
    lines_added: <integer>
    lines_deleted: <integer>
    description: <what_was_done>

outputs:
  files_created:
    - <path1>
    - <path2>
  files_modified:
    - <path3>
    - <path4>
  tests_added: <integer>
  docs_updated: <integer>

validation:
  schema_compliance: true|false
  front_matter_valid: true|false
  tests_pass: true|false
  ci_status: pass|fail|pending

acceptance_checklist:
  - item: SI units used
    status: ✅|⚠️|❌
  - item: CHBDC/CSA cited
    status: ✅|⚠️|❌
  - item: Front-matter present
    status: ✅|⚠️|❌
  - item: Tests included
    status: ✅|⚠️|❌
  - item: Docs updated
    status: ✅|⚠️|❌
  - item: Changelog updated
    status: ✅|⚠️|❌

review:
  reviewed_by: <human_name>
  review_date: YYYY-MM-DD
  status: approved|changes_requested|rejected
  comments: <optional_notes>

metrics:
  files_touched: <integer>
  total_lines_changed: <integer>
  session_duration_min: <integer>
  guardrails_triggered: <list_or_none>

notes: |
  Optional free-form notes about the session
---
```

---

## Field Definitions

### Required Fields (Minimal Log)
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `session_id` | string | Unique ID: `YYYY-MM-DD-<slug>` | `2025-10-05-adr-creation` |
| `date` | date | ISO format date | `2025-10-05` |
| `actor` | string | AI agent or human name | `Claude Code`, `Human` |
| `phase` | integer | Current plan phase | `0`, `1`, `2` |
| `outputs` | object | Files created/modified | See below |

### Outputs Object
```yaml
outputs:
  files_created: [<paths>]     # List of new files
  files_modified: [<paths>]    # List of edited files
  tests_added: <integer>       # Number of test cases added
  docs_updated: <integer>      # Number of docs updated
```

### Acceptance Checklist
Every session must verify:
- ✅ SI units used internally
- ✅ CHBDC/CSA citations where applicable
- ✅ YAML front-matter present on docs
- ✅ Tests included for code changes
- ✅ Documentation updated
- ✅ CHANGELOG.md updated

Status codes:
- `✅` Pass
- `⚠️` Partial (explain in notes)
- `❌` Fail

### Validation Object
```yaml
validation:
  schema_compliance: <boolean>      # YAML front-matter valid
  front_matter_valid: <boolean>     # All required fields present
  tests_pass: <boolean>             # pytest succeeded
  ci_status: pass|fail|pending      # GitHub Actions result
```

### Review Object
```yaml
review:
  reviewed_by: <string>             # Human reviewer name
  review_date: YYYY-MM-DD           # Review date
  status: approved|changes_requested|rejected
  comments: <string>                # Optional feedback
```

---

## Guardrail Compliance

Sessions must respect:
- **File cap**: ≤12 files modified
- **Line cap**: ≤600 lines changed
- **Path allowlist**: Only approved directories
- **Stop rule**: Halt after 2 consecutive CI failures

If guardrails are triggered, log in `metrics.guardrails_triggered`:
```yaml
metrics:
  guardrails_triggered:
    - file_cap_exceeded: 15 files (cap: 12)
    - line_cap_exceeded: 720 lines (cap: 600)
```

---

## Validation Rules

A log entry is valid if:
1. All required fields present
2. Date in ISO format `YYYY-MM-DD`
3. Phase number matches active plan
4. Outputs list all modified files
5. Acceptance checklist completed
6. Guardrails not exceeded (or violation documented)

---

## Example: Minimal Session Log

```yaml
---
session_id: 2025-10-05-create-adrs
date: 2025-10-05
actor: Claude Code
phase: 0
plan_reference: docs/framework/1-governance/simple-span-framework-refinement-plan-v5.0.md

outputs:
  files_created:
    - docs/framework/1-governance/adrs/ADR-001-SI-units-and-metric.md
    - docs/framework/1-governance/adrs/ADR-002-layer-architecture.md
    - docs/framework/1-governance/adrs/ADR-003-semantic-versioning.md
    - docs/framework/1-governance/adrs/ADR-004-domain-granularity.md
    - docs/framework/1-governance/adrs/ADR-005-ai-governance-integration.md
    - docs/framework/1-governance/adrs/ADR-006-testing-and-validation-strategy.md
  files_modified: []
  tests_added: 0
  docs_updated: 6

validation:
  schema_compliance: true
  front_matter_valid: true
  tests_pass: true
  ci_status: pending

acceptance_checklist:
  - item: SI units used
    status: ✅
  - item: Front-matter present
    status: ✅
  - item: Docs updated
    status: ✅
---
```

---

## Example: Detailed Session Log

```yaml
---
session_id: 2025-10-05-implement-section-props
date: 2025-10-05
time_start: 14:30:00
time_end: 16:15:00
actor: Claude Code
agent_type: implementer
plan_reference: examples/plans/section-properties-plan-sample.md
phase: 2

context_loaded:
  - docs/framework/1-governance/coding-implementation-standards.md
  - docs/framework/2-validation/validation-verification-manual.md
  - docs/framework/1-governance/adrs/ADR-001-SI-units-and-metric.md
  - examples/plans/section-properties-plan-sample.md

intent:
  goal: Implement rectangular section properties calculator
  type: module
  scope: section-properties

actions:
  - action: create
    file: src/domain/section_properties/rectangular.py
    lines_added: 85
    lines_deleted: 0
    description: Implement rectangle section class with A, Ix, Iy calculations
  - action: create
    file: tests/unit/section_properties/test_rectangular.py
    lines_added: 120
    lines_deleted: 0
    description: Add unit tests with SI units and tolerances
  - action: create
    file: tests/validation/section_properties/cases/rect-001.json
    lines_added: 18
    lines_deleted: 0
    description: Add validation case for 300x600 rectangle

outputs:
  files_created:
    - src/domain/section_properties/rectangular.py
    - tests/unit/section_properties/test_rectangular.py
    - tests/validation/section_properties/cases/rect-001.json
  files_modified: []
  tests_added: 8
  docs_updated: 0

validation:
  schema_compliance: true
  front_matter_valid: true
  tests_pass: true
  ci_status: pass

acceptance_checklist:
  - item: SI units used
    status: ✅
  - item: CHBDC/CSA cited
    status: ⚠️  # Not applicable for pure geometry
  - item: Front-matter present
    status: ✅
  - item: Tests included
    status: ✅
  - item: Docs updated
    status: ⚠️  # Module docs to be added in next session
  - item: Changelog updated
    status: ✅

review:
  reviewed_by: Human
  review_date: 2025-10-05
  status: approved
  comments: Tests pass, calculations verified

metrics:
  files_touched: 3
  total_lines_changed: 223
  session_duration_min: 105
  guardrails_triggered: none

notes: |
  Implemented basic rectangular section properties.
  Next session: Add composite sections and holes.
---
```

---

## Storage Locations

### Primary Log:
- `reports/progress.md` — Required one-line entries

### Detailed Logs (optional):
- `reports/ai/sessions/<YYYY>/<MM>/<session_id>.yaml`
- Organize by year/month for scalability

### Aggregated Reports:
- `reports/ai/ai-summary-YYYY-MM.md` — Monthly summaries
- `reports/ai/ai-summary-YYYY-MM.csv` — Metrics export
- Generated by `tools/ai/ai_summary.py`

---

## CI Integration

### Automated Checks:
1. **Front-matter validation**: `tools/docs_audit.py --check-ai-logs`
2. **Schema validation**: Verify YAML structure
3. **Guardrail check**: Ensure caps not exceeded
4. **Completeness**: All AI-generated files have log entries

### Workflow:
```yaml
- name: Validate AI Logs
  run: |
    python tools/docs_audit.py --strict --check-ai-logs
    python tools/ai/validate_session_logs.py
```

---

## Related Schemas
- **Plan Schema**: `docs/framework/ai/plan-schema.md`
- **Front-matter Schema**: See governance docs YAML requirements
- **AI Router Schema**: `tools/ai/router-map.schema.json`

---

## Versioning
- **Current**: v1.0
- **Changes** require updating `schema_version` field
- **Backward compatibility**: Tools support N and N-1 versions

---

*Prepared by SimpleSpan Core Governance — 2025-10-05*
