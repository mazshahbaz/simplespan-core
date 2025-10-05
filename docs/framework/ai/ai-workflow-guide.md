---
title: AI Development Workflow — Operational Guide
version: 1.0
context: ai/workflow
last_reviewed: 2025-10-05
ai_context: true
supersedes:
  - ai-development-sop.md
  - context-bootstrap.md
  - CONTRIBUTING-AI-ADDENDUM.md
---

# AI Development Workflow — Operational Guide

**Purpose**: This is THE definitive guide for all AI-assisted development in SimpleSpan. It consolidates workflows, commands, and best practices into a single operational reference.

**Who**: AI agents (Claude Code, Cursor, GPT) and human engineers working collaboratively.

**Authority**: Governed by ADR-005 (AI Governance Integration).

---

## Quick Reference

```bash
# Start a new AI session
python tools/ai/route_task.py --type plan --subtype module --goal "section properties"

# Validate documentation
python tools/docs_audit.py --strict --check-links --check-ai-logs

# Check progress
cat reports/progress.md

# Run AIC Orchestrator (get next tasks)
python tools/aic_orchestrator.py
```

---

## The 6-Step Workflow

All AI work follows this mandatory cycle:

```
┌─────────┐
│  PLAN   │ → Define scope, acceptance criteria
└────┬────┘
     ↓
┌─────────┐
│ EXECUTE │ → Implement with AI, following standards
└────┬────┘
     ↓
┌─────────┐
│ REVIEW  │ → Human + CI validation
└────┬────┘
     ↓
┌─────────┐
│  MERGE  │ → Integrate to main branch
└────┬────┘
     ↓
┌─────────┐
│  AUDIT  │ → Automated compliance checks
└────┬────┘
     ↓
┌─────────┐
│ SUMMARY │ → Monthly reporting
└─────────┘
```

---

## Step 1: PLAN

### Goal
Define what will be built, with clear acceptance criteria and context.

### Commands
```bash
# For a new domain module
python tools/ai/route_task.py --type plan --subtype module --goal "section properties v0.1"

# For a feature within existing module
python tools/ai/route_task.py --type plan --subtype feature --goal "composite sections with holes"
```

### What the Router Does
1. Generates planning prompt from template
2. Loads required context documents
3. Outputs acceptance checklist
4. Creates `.ai/last_prompt.txt` and `.ai/context-files.txt`

### Planning Deliverables
For **modules** (full domain):
- `module-requirements.md` — Scope, inputs/outputs, CHBDC references
- `module-design-brief.md` — Architecture, API, algorithms
- `validation-plan.md` — Test cases with references and tolerances
- `module-roadmap.md` — Milestones and acceptance gates

For **features** (enhancements):
- Feature spec with inputs/outputs
- Test plan
- Update plan for existing docs

### Acceptance Checklist (Planning)
- [ ] SI units specified for all physical quantities
- [ ] CHBDC/CSA clauses cited where applicable
- [ ] Inputs, outputs, and units documented
- [ ] Validation cases identified with references
- [ ] Dependencies on other modules clear
- [ ] Roadmap with measurable acceptance criteria

### Human Action
**Review the plan** and approve before proceeding to Execute.

---

## Step 2: EXECUTE

### Goal
Implement code, tests, and documentation following the approved plan.

### Session Initialization

#### Load Context Documents
Before generating code, ensure AI has loaded:

**Always Required**:
1. `docs/framework/1-governance/coding-implementation-standards.md`
2. `docs/framework/1-governance/software-architecture-guide.md`
3. `docs/framework/2-validation/validation-verification-manual.md`
4. `docs/framework/1-governance/adrs/ADR-001-SI-units-and-metric.md`
5. `docs/framework/1-governance/adrs/ADR-002-layer-architecture.md`
6. The approved plan document

**Module-Specific**:
7. Relevant ADRs (ADR-004 for domain modules, ADR-006 for testing)
8. Related module documentation
9. Example validation cases

#### Verify Context
AI agent must confirm:
- Current phase from active plan (`simple-span-framework-refinement-plan-v5.0.md`)
- Last CCP from `reports/progress.md`
- Guardrails understood (≤12 files, ≤600 lines, allowlisted paths)

### Implementation Standards

#### Code Requirements
- **SI units internally** (ADR-001): kN, m, mm, MPa
- **Layer boundaries** (ADR-002): No upward dependencies
- **Typed interfaces**: Use type hints for all public APIs
- **Docstrings**: Google/NumPy style with units and CHBDC references
- **Error handling**: Explicit exceptions with actionable messages

#### Example Docstring
```python
def flexural_capacity_kNm(fc_mpa: float, b_mm: float, d_mm: float) -> float:
    """Compute factored flexural capacity per CSA A23.3-19.

    Args:
        fc_mpa: Concrete compressive strength (MPa). Range: 20-80.
        b_mm: Section width (mm). Must be > 0.
        d_mm: Effective depth (mm). Must be > 0.

    Returns:
        Factored moment capacity (kN·m).

    Raises:
        ValueError: If inputs outside valid ranges.

    References:
        CSA A23.3-19 Clause 10.1.7
    """
```

#### Test Requirements (ADR-006)
For every code change:
1. **Unit tests**: Test functions in isolation
2. **Validation tests**: Compare to CHBDC/CSA examples (JSON format)
3. **Edge cases**: Test boundary conditions and error handling

#### Example Validation Case
```json
{
  "id": "SPN-SEC-001",
  "title": "Rectangular section properties",
  "reference": "CHBDC Commentary Example 5.2",
  "inputs": {
    "b_mm": 300.0,
    "h_mm": 600.0
  },
  "expected": {
    "area_mm2": 180000.0,
    "Ix_mm4": 5.4e9
  },
  "tolerances": {
    "relative": 1e-6,
    "absolute": 1e-9
  }
}
```

#### Documentation Requirements
- **YAML front-matter** on all docs:
  ```yaml
  ---
  title: Document Title
  version: 1.0
  context: area/topic
  last_reviewed: 2025-10-05
  ai_generated: true
  ---
  ```
- **Update CHANGELOG.md**: Add entry for changes
- **Module README**: Overview, usage, references

### Guardrails (Enforced)
- **File limit**: ≤12 files modified per session
- **Line limit**: ≤600 lines changed per session
- **Path allowlist**: Only modify approved directories:
  - `docs/**`
  - `src/**`
  - `tests/**`
  - `tools/**`
  - `reports/**`
- **Stop rule**: Halt after 2 consecutive CI failures

### Logging Required
Add entry to `reports/progress.md`:
```
2025-10-05 | Claude Code | Phase 2 | v5.0 | Implemented rectangular section properties | — | —
```

### Acceptance Checklist (Execution)
- [ ] SI units used internally
- [ ] CHBDC/CSA citations in docstrings where applicable
- [ ] YAML front-matter on all new docs
- [ ] Unit tests written and passing
- [ ] Validation tests with JSON cases included
- [ ] CHANGELOG.md updated
- [ ] Session logged in progress.md
- [ ] Guardrails respected

---

## Step 3: REVIEW

### Goal
Human engineer validates correctness, AI agent validates compliance.

### Human Review Checklist
**Engineering Correctness**:
- [ ] Calculations align with CHBDC/CSA provisions
- [ ] Assumptions documented and reasonable
- [ ] Edge cases handled appropriately
- [ ] Physical units make sense

**Code Quality**:
- [ ] Follows coding standards (ADR-002)
- [ ] Clear variable names
- [ ] Appropriate error handling
- [ ] Tests cover critical paths

**Documentation**:
- [ ] API clearly documented
- [ ] Examples provided
- [ ] References accurate

### Automated Review (CI)
```bash
# Run full validation
python tools/docs_audit.py --strict --check-links --check-ai-logs

# Run tests
pytest -q --cov=simplespan_core

# Run linter
ruff check .

# Run type checker
mypy src
```

### CI Must Pass
- Lint (ruff): No errors
- Tests (pytest): All passing
- Type check (mypy): No errors (gradually enforced)
- Docs audit: Front-matter valid, links working
- Coverage: ≥80% for domain/core

### Review Outcomes
- **Approved**: Proceed to Merge
- **Changes Requested**: Return to Execute with specific feedback
- **Rejected**: Return to Plan if fundamental issues

---

## Step 4: MERGE

### Goal
Integrate approved changes to main branch.

### Pre-Merge Checklist
- [ ] CI green (all checks passing)
- [ ] Human review approved
- [ ] CHANGELOG.md updated
- [ ] Progress log entry exists
- [ ] Version updated if needed (ADR-003)

### Merge Process
```bash
# Ensure branch is up to date
git fetch origin
git rebase origin/main

# Run final validation
pytest -q
python tools/docs_audit.py --strict

# Commit if not already
git add .
git commit -m "Add section properties module

Implements rectangular and circular section calculations per ADR-004.
Includes validation against CHBDC Commentary examples.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push and create PR
git push -u origin <branch-name>
gh pr create --title "Add section properties module" --body "..."
```

### PR Requirements
- **Title**: Clear, concise description
- **Body**:
  - Summary of changes
  - Link to plan document
  - Test plan/validation
  - Breaking changes (if any)
- **Checks**: All CI workflows green

---

## Step 5: AUDIT

### Goal
Automated verification of compliance and documentation.

### Automated Checks (CI)
These run automatically on merge:

1. **Docs Audit**: Validates front-matter, links, AI logs
2. **Schema Validation**: Ensures YAML structure correct
3. **Test Coverage**: Verifies coverage targets met
4. **License Check**: Ensures all files properly attributed

### Manual Audit (Optional)
For critical modules:
```bash
# Generate comprehensive audit
python tools/docs_audit.py --strict --check-links --check-ai-logs --verbose

# Review validation evidence
ls -la tests/validation/<module>/cases/

# Check test coverage detail
pytest --cov=simplespan_core --cov-report=html
```

### Audit Artifacts
- `reports/docs_audit_report.json` — Documentation audit results
- `reports/coverage.html` — Test coverage report
- `reports/ai/sessions/` — Detailed session logs (optional)

---

## Step 6: MONTHLY SUMMARY

### Goal
Generate aggregate metrics and reports for governance review.

### Automated (CI - 1st of each month)
```bash
python tools/ai/ai_summary.py --month $(date +'%Y-%m') --out reports/ai --csv
```

### Generates
- `reports/ai/ai-summary-YYYY-MM.md` — Human-readable summary
- `reports/ai/ai-summary-YYYY-MM.csv` — Metrics for analysis

### Metrics Tracked
- Number of AI sessions
- Files created/modified
- Lines of code generated
- Test coverage added
- CI pass rate
- Review acceptance rate
- Schema compliance rate
- Guardrail violations

### Governance Review
Monthly review examines:
- AI productivity and quality trends
- Common failure patterns
- Guardrail effectiveness
- Documentation compliance
- Areas for process improvement

---

## Common Workflows

### Workflow A: New Domain Module

```bash
# 1. PLAN
python tools/ai/route_task.py --type plan --subtype module --goal "beam analysis module"
# → Review generated planning docs, approve

# 2. EXECUTE
# → AI loads context, implements per plan
# → Generates src/domain/beam_analysis/*.py
# → Generates tests/unit/beam_analysis/test_*.py
# → Generates tests/validation/beam_analysis/cases/*.json
# → Updates CHANGELOG.md, logs to progress.md

# 3. REVIEW
pytest tests/unit/beam_analysis/
python tools/docs_audit.py --strict
# → Human reviews engineering correctness

# 4. MERGE
git checkout -b feat/beam-analysis
git add .
git commit -m "Add beam analysis module"
git push -u origin feat/beam-analysis
gh pr create

# 5. AUDIT (automatic on merge)
# 6. SUMMARY (automatic monthly)
```

### Workflow B: Feature Addition

```bash
# 1. PLAN
python tools/ai/route_task.py --type plan --subtype feature --goal "add composite sections to section-properties"

# 2. EXECUTE
# → AI extends existing module
# → Adds tests and validation cases
# → Updates module docs

# 3-6. Same as Workflow A
```

### Workflow C: Bug Fix

```bash
# 1. PLAN (lightweight for bugs)
# → Document issue, expected vs. actual behavior

# 2. EXECUTE
# → Fix code
# → Add regression test in tests/regression/test_issue_NN.py
# → Update CHANGELOG.md

# 3-6. Same as Workflow A
```

---

## AIC Orchestrator Usage

The AIC Orchestrator helps manage multi-phase work.

### Check Next Tasks
```bash
# View next 1-3 tasks from active plan
python tools/aic_orchestrator.py

# Get specific phase
python tools/aic_orchestrator.py --phase 2 --max-tasks 3

# JSON output for automation
python tools/aic_orchestrator.py --json
```

### Orchestrator Output
Provides:
- Current phase and completion %
- Next actionable tasks (micro-tasks)
- Context files to load
- Acceptance criteria to verify
- CCP proposal when phase complete

---

## Troubleshooting

### "Guardrail exceeded: file cap"
**Solution**: Break work into smaller sessions. Commit intermediate state.

### "CI failing: docs_audit front-matter invalid"
**Solution**: Ensure all docs have required YAML front-matter:
```yaml
---
title: <string>
version: <semver>
context: <area>
last_reviewed: YYYY-MM-DD
ai_generated: true  # if AI-created
---
```

### "Tests failing after code generation"
**Solution**:
1. Review test output for specific failures
2. Check SI units are used internally
3. Verify validation tolerance settings
4. Ensure CHBDC references match test cases

### "Import error: circular dependency"
**Solution**: Verify layer dependencies (ADR-002). Domain cannot import Application/Presentation.

---

## Best Practices

### DO
✅ Load all required context documents before starting
✅ Follow the 6-step workflow strictly
✅ Log every session in progress.md
✅ Write tests for all code changes
✅ Use SI units internally
✅ Cite CHBDC/CSA clauses in docstrings
✅ Keep sessions small (≤12 files, ≤600 lines)
✅ Update CHANGELOG.md

### DON'T
❌ Skip the planning step
❌ Merge without CI passing
❌ Generate code without tests
❌ Mix units (use SI internally only)
❌ Create circular dependencies
❌ Exceed guardrail caps in one session
❌ Skip human review
❌ Forget to update documentation

---

## Quick Commands Cheat Sheet

```bash
# Planning
python tools/ai/route_task.py --type plan --subtype module --goal "<goal>"

# Validation
python tools/docs_audit.py --strict --check-links --check-ai-logs
pytest -q --cov=simplespan_core
ruff check .
mypy src

# Progress
cat reports/progress.md
python tools/aic_orchestrator.py

# Summaries
python tools/ai/ai_summary.py --month $(date +'%Y-%m') --out reports/ai --csv

# Git workflow
git checkout -b <branch>
git add .
git commit -m "<message>"
git push -u origin <branch>
gh pr create
```

---

## Related Documentation

- **ADR-005**: AI Governance Integration (authority)
- **Plan Schema**: `docs/framework/ai/plan-schema.md`
- **Logging Schema**: `docs/framework/ai/logging-schema.md`
- **Coding Standards**: `docs/framework/1-governance/coding-implementation-standards.md`
- **Validation Manual**: `docs/framework/2-validation/validation-verification-manual.md`
- **AIC Sub-Project**: `docs/framework/ai/aic-subproject/README.md`

---

*This guide is the single source of truth for AI development in SimpleSpan. All other AI workflow documents are superseded or archived.*

**Last Updated**: 2025-10-05
**Maintained By**: SimpleSpan Governance Board
