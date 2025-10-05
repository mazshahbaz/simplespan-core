# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SimpleSpan Core** is a Python-based structural engineering framework using **SI units** and aligned with **Canadian codes (CHBDC/CSA)**. The project is optimized for AI-assisted development (Cursor, Claude) with strict governance, validation, and traceability requirements.

**Philosophy**: Correctness > Maintainability > Performance

## Development Commands

### Setup
```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests with coverage
pytest -q --cov=simplespan_core

# Run specific test directory
pytest tests/unit/
pytest tests/validation/

# Run single test file
pytest tests/unit/test_specific.py

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Lint code
ruff check .

# Type check (gradual adoption)
mypy src

# Build package
python -m build
```

### Documentation & AI Tools
```bash
# Audit documentation (front-matter, links, AI logs)
python tools/docs_audit.py --strict --check-links --check-ai-logs

# AI task router (for planning/scaffolding)
python tools/ai/route_task.py --type plan --subtype module --goal "feature description"
python tools/ai/route_task.py --type plan --subtype feature --goal "feature description"

# AI summary and audit
python tools/ai/ai_summary.py --month $(date +'%Y-%m') --out reports/ai --csv

# AIC Orchestrator (task coordination)
python tools/aic_orchestrator.py
python tools/aic_orchestrator.py --phase 3 --max-tasks 2
```

## Architecture

SimpleSpan uses a **5-layer architecture** with **strict one-way dependencies** (no upward imports):

```
Presentation  (UI, API, CLI)
     ↓
Application   (orchestration, workflows)
     ↓
Domain        (engineering calculations - section-properties, beam-analysis, etc.)
     ↓
Infrastructure (IO, persistence, logging, config)
     ↓
Core          (math, geometry, materials, units, validation utils)
```

### Repository Structure
```
src/
├─ core/               # Foundational libraries (math, geometry, materials, units)
├─ domain/             # Structural engineering modules
│  ├─ section-properties/
│  ├─ beam-analysis/
│  ├─ prestressing/
│  └─ ...
├─ infrastructure/     # Technical services (data-access, io, config)
├─ application/        # Orchestration (beam-app, section-app)
└─ presentation/       # UI/API layers (desktop, web, cli)

tests/
├─ unit/               # Function-level tests
├─ validation/         # CHBDC/CSA reference cases
├─ integration/        # Multi-module workflows
└─ regression/         # Fixed bugs (locked forever)

docs/
├─ framework/
│  ├─ 1-governance/    # Handbook, architecture, coding standards
│  ├─ 2-validation/    # V&V manual
│  ├─ 3-libraries/     # Shared library integration
│  └─ 4-execution/     # Prompt library for AI
└─ whitepapers/

data/                  # Materials DBs, section libraries, validation datasets
```

### Domain Module Pattern
Each domain module follows this structure:
```
src/domain/<module-name>/
  ├─ __init__.py
  ├─ <module_name>.py       # Main implementation
  ├─ interfaces.py          # Typed function/class interfaces
  ├─ algorithms.py          # Core calculations (pure functions)
  ├─ validators.py          # Input validation and units checks
  └─ README.md

docs/modules/<module-name>/
  ├─ overview.md            # Purpose, scope, assumptions
  ├─ interfaces.md          # API, units, error cases
  ├─ algorithms.md          # Method details with CHBDC/CSA references
  ├─ validation.md          # Test cases, tolerances, references
  └─ changelog.md

tests/unit/<module-name>/test_*.py
tests/validation/<module-name>/cases/*.json
```

## AI Development Workflow

All AI-assisted development follows a **mandatory 6-step cycle**. See **[`docs/framework/ai/ai-workflow-guide.md`](docs/framework/ai/ai-workflow-guide.md)** for the complete operational guide.

**Quick workflow**:

1. **Plan** — Use AI Router to generate context and prompts
   ```bash
   python tools/ai/route_task.py --type plan --subtype module --goal "Section Properties v0.1"
   ```

2. **Execute** — Follow acceptance checklist; add `ai_generated: true` to YAML front-matter

3. **Review** — Human review required; run `python tools/docs_audit.py`

4. **Merge** — Only after CI passes and CHANGELOG updated

5. **Audit** — Automated documentation and AI log verification

6. **Monthly Summary** — `ai_summary.py` generates reports

### AI-Generated File Requirements
All AI-created markdown files must include YAML front-matter:
```yaml
---
title: File Title
version: 1.0
context: framework/category
last_reviewed: YYYY-MM-DD
ai_generated: true
---
```

## Coding Standards

### Python Conventions
- **Python 3.11+** required
- **PEP 8** + project-specific standards
- **Naming**:
  - Packages/modules: `snake_case`
  - Classes: `PascalCase` (use sparingly; prefer functions)
  - Functions/variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: prefix with `_`

### Units Policy (MANDATORY)
- **SI units internally**: N, kN, m, mm, MPa, kN·m
- **Convert only at boundaries** (presentation/infrastructure layers)
- **Include units in variable names when ambiguous**: `moment_kNm`, `stress_mpa`, `length_mm`
- **Document units in docstrings** for all physical quantities

### Docstrings
Use Google or NumPy style. **Always specify units and CHBDC/CSA references**:
```python
def flexural_capacity_m_kNm(fc_mpa: float, fy_mpa: float, b_mm: float, d_mm: float) -> float:
    """Compute factored flexural capacity (φMn) in kN·m.

    Args:
        fc_mpa: Concrete compressive strength (MPa).
        fy_mpa: Steel yield strength (MPa).
        b_mm: Section width (mm).
        d_mm: Effective depth (mm).

    Returns:
        Factored moment capacity (kN·m).

    References:
        CSA A23.3-19 Clause 10.x; CHBDC S6-19 Section Y.Z

    Raises:
        ValueError: If inputs are non-positive or outside typical ranges.
    """
```

### Error Handling
- Validate all public inputs
- Raise `ValueError`, `TypeError`, or domain-specific exceptions
- Messages must be **actionable**: include parameter name, value, expected range/units
- No silent failures

### Dependencies
- **No upward imports** across layers (e.g., domain cannot import application)
- Absolute imports within package
- Minimal external dependencies; prefer standard library

## Testing Requirements

### Unit Tests
- Test every function/class with edge cases
- Use numeric **tolerances** for floats
- Helper function pattern:
```python
def almost_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
```

### Validation Tests
Location: `tests/validation/<module>/cases/*.json`

JSON structure:
```json
{
  "id": "SPN-001",
  "title": "Rectangular section properties",
  "inputs": { "b_mm": 300.0, "h_mm": 600.0 },
  "expected": { "area_mm2": 180000.0, "Iy_mm4": 3.24e9 },
  "tolerances": { "relative": 1e-6, "absolute": 1e-9 },
  "reference": "CHBDC Example X.Y or Textbook Reference"
}
```

Test code loads JSON, runs module, asserts within tolerance.

### Reference Hierarchy
1. **CHBDC/CSA clauses** and official examples (primary)
2. Peer-reviewed textbooks and publications
3. Analytical solutions (closed-form)
4. Cross-checked numerical results from independent tools

## Documentation Standards

### Markdown Front-matter (Required)
All documentation files under `docs/` must include:
```yaml
---
title: Document Title
version: 1.0
context: framework/category
last_reviewed: YYYY-MM-DD
audience: structural_engineers, software_engineers, ai_agents
units: SI (metric)
codes: [CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19]
ai_generated: true  # if AI-created
---
```

### Key Documents
- `docs/framework/1-governance/software-development-handbook.md` — Governing principles
- `docs/framework/1-governance/software-architecture-guide.md` — Architecture details
- `docs/framework/1-governance/coding-implementation-standards.md` — Python standards
- `docs/framework/2-validation/validation-verification-manual.md` — V&V process
- `docs/framework/quick-start.md` — Development workflow overview

## CI/CD

GitHub Actions workflows:
- **ci.yml**: Lint (ruff), type check (mypy), tests (pytest with coverage)
- **tests.yml**: Extended test suite
- **docs-audit.yml**: Verify documentation front-matter and links
- **router-map-lint.yml**: Validate AI router configuration
- **ai-summary.yml**: Monthly AI activity reports

All checks must pass before merge to main.

## Key References

- **Codes**: CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19
- **Units**: SI exclusively (N, kN, m, mm, MPa, kN·m) — See ADR-001
- **Layering**: One-way dependencies enforced (Core → Infrastructure → Domain → Application → Presentation) — See ADR-002
- **Versioning**: Semantic Versioning (MAJOR.MINOR.PATCH) — See ADR-003
- **Domain Modules**: Granular, validated, CHBDC-mapped modules — See ADR-004
- **AI Governance**: Mandatory 6-step workflow with logging — See ADR-005
- **Testing**: 4-tier strategy (unit, integration, validation, regression) — See ADR-006

### Architecture Decision Records (ADRs)

Essential ADRs are located in `docs/framework/1-governance/adrs/`:
- **ADR-001**: SI Units and Metric System
- **ADR-002**: Five-Layer Architecture and Dependency Rules
- **ADR-003**: Semantic Versioning
- **ADR-004**: Domain Module Granularity
- **ADR-005**: AI Governance Integration
- **ADR-006**: Testing and Validation Strategy

### Active Plan

Current framework roadmap: `docs/framework/1-governance/simple-span-framework-refinement-plan-v5.0.md`
- **Current Phase**: 0 (Continuity & Genesis)
- **Progress Tracking**: `reports/progress.md`
- **Legacy Plans**: Archived in `docs/framework/1-governance/archive/`
