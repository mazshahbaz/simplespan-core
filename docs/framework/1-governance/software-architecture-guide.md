---
title: Software Architecture & Module Design Guide
version: 1.0
brand: SimpleSpan Software
repo: simplespan-core
context: framework/architecture
audience: structural_engineers, software_engineers, ai_agents
units: SI (metric)
codes: [CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19]
related:
  - ./coding-implementation-standards.md
  - ../2-validation/validation-verification-manual.md
---

© 2025 SimpleSpan Software. All rights reserved.

# 0. Purpose
Define the **modular architecture, layering rules, dependency policy, and design workflow** for SimpleSpan Core (Python). This guide ensures correctness, maintainability, and **AI-friendly modularity**.

# 1. Architectural Principles
1. **Correctness > Maintainability > Performance > Convenience.**
2. **Layered design with one-way dependencies.**
3. **Small, composable modules** with explicit interfaces.
4. **Pure domain logic** free of UI/IO.
5. **Deterministic computations** with explicit units (SI) and references.

# 2. Layering Model (One-Way Dependencies)

```
+----------------------+   Presentation (UI, API, CLI)
|   PRESENTATION       |   - No domain logic
+----------+-----------+
           v
+----------------------+   Application (orchestration/workflows)
|   APPLICATION        |   - Coordinates domain modules
+----------+-----------+
           v
+----------------------+   Domain (engineering logic, equations)
|   DOMAIN             |   - Pure, validated, unit-aware
+----------+-----------+
           v
+----------------------+   Infrastructure (IO, DB, logging, config)
|   INFRASTRUCTURE     |   - Adapters, persistence, services
+----------+-----------+
           v
+----------------------+   Core (math, geometry, materials, units)
|   CORE               |   - Foundations, utilities
+----------------------+
```

**Rules:**  
- No upward imports. Example: `domain` can import `core` but **never** `presentation`.  
- `domain` must not import `presentation` or `application`.  
- `application` orchestrates; `domain` computes; `infrastructure` adapts.

# 3. Repository Mapping

```
src/
├─ core/                 # math, geometry, materials, units, validation utils
├─ domain/               # section-properties, beam-analysis, prestressing, ...
├─ infrastructure/       # data-access, io, config, logging, rendering
├─ application/          # beam-app, section-app, shared orchestration
└─ presentation/         # desktop, web, cli
```

# 4. Module Blueprint (Per Domain Module)

**File/Folder Layout:**
```
src/domain/<module-name>/
  ├─ __init__.py
  ├─ <module_name>.py
  ├─ interfaces.py           # typed function/class interfaces
  ├─ algorithms.py           # core calculations (pure)
  ├─ validators.py           # input validation and units checks
  └─ README.md               # short overview
docs/modules/<module-name>/
  ├─ overview.md             # purpose, scope, assumptions
  ├─ interfaces.md           # API + units + error cases
  ├─ algorithms.md           # method details with code references
  ├─ validation.md           # cases, tolerances, references
  └─ changelog.md
tests/unit/<module-name>/test_*.py
tests/validation/<module-name>/cases/*.json
```

**Module Doc Template (AI-friendly anchors):**
```
# Overview
# Responsibilities
# Interfaces
# Dependencies
# Algorithms (with CHBDC/CSA references)
# Validation (cases + tolerances)
# Examples (Python)
# Changelog
```

# 5. Interface & Data Contracts
- **Typed function signatures** with docstrings listing **units** and **references**.
- Data contracts in JSON for validation cases (store SI with metadata).
- Avoid optional/implicit units; require explicit SI inputs.

# 6. Dependency Policy
- Allowed imports for each layer (subset of below):

```
core           -> standard library only
infrastructure -> core
domain         -> core (+ specific infra adapters *via interfaces*)
application    -> domain, infrastructure
presentation   -> application
```

- **No circular dependencies.** Use interfaces/abstraction for cross-calls.
- **Dependency Inversion**: application depends on abstractions, not concrete infra.

# 7. Design Workflow (9 Phases)
1. **Intent** — define problem, scope, success criteria.
2. **Inputs/Outputs** — list parameters with **units**; define SI only.
3. **Standards** — cite CHBDC/CSA clauses and equations.
4. **Assumptions/Limits** — define applicability (e.g., linear elastic range).
5. **Data Model** — select data types and JSON schema (if needed).
6. **Interfaces** — design public API; raise precise exceptions.
7. **Algorithms** — derive/choose methods; document references.
8. **Validation Plan** — choose cases, define tolerances.
9. **Integration Plan** — how the module plugs into application workflows.

# 8. Example: Section Properties Module (Sketch)

**Interface (Python):**
```python
def compute_section_properties(polygon_mm: list[tuple[float, float]]) -> dict:
    """Compute area, centroid, and second moments in SI.
    Inputs: polygon_mm (outer boundary, mm)
    Returns: {area_mm2, cx_mm, cy_mm, Iy_mm4, Iz_mm4}
    References: Mechanics of Materials; CSA A23.3-19 (geometry context)
    Raises: ValueError on self-intersection or degenerate polygon.
    """
```

**ASCII Flow:**
```
[polygon_mm] --> [validators] --> [algorithms: area, centroid, Ix, Iy] --> [results dict]
                                  ^                                     |
                                  |________________ error handling _____|
```

# 9. Diagrams & Conventions (ASCII)
- Use monospaced block diagrams for flows and layer maps (examples above).
- Store any richer diagrams under `/docs/diagrams/` with a matching filename.

# 10. Review Checklist (Architecture)
- [ ] Inputs/outputs & units defined
- [ ] References cited (CHBDC/CSA)
- [ ] Pure domain logic (no IO/UI)
- [ ] Interfaces stable & typed
- [ ] Validation plan + tolerances
- [ ] No circular dependencies

# 11. References
- CHBDC CSA S6-19, CSA A23.3-19, CSA S16-19.
- *Mechanics of Materials*; *Reinforced Concrete: Mechanics & Design*.