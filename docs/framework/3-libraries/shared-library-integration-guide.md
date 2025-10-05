
---
title: Shared Library Integration Guide
version: 1.0
brand: SimpleSpan Software
context: framework/shared-libraries
audience: structural_engineers, software_engineers, ai_agents, qa
units: SI (metric)
codes: [CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19]
related:
  - ../3-libraries/data-schema-and-interchange-standard.md
  - ../../4-execution/documentation-and-knowledge-management-guide.md
---

© 2025 SimpleSpan Software. All rights reserved.

# 0. Purpose
Define how **shared libraries** are designed, versioned, validated, and integrated across all
SimpleSpan projects.  
These rules ensure that reusable components (math, materials, geometry, validation, etc.)
remain **consistent, verifiable, and maintainable** across the ecosystem.

---

# 1. Principles

1. **Single Source of Truth** — every algorithm, constant, or dataset must exist in exactly one authoritative package.  
2. **Backward Compatibility by Design** — updates never break validated modules without a documented migration.  
3. **Semantic Versioning (SemVer)** governs all releases (`MAJOR.MINOR.PATCH`).  
4. **Explicit Dependencies Only** — each library declares its requirements via `pyproject.toml`.  
5. **Layer Isolation** — shared libraries never depend upward on domain or presentation code.  
6. **Determinism & Auditability** — identical inputs always yield identical results across versions.

---

# 2. Shared Library Taxonomy

| Library | Responsibility | Example Folder |
|----------|----------------|----------------|
| **core-math** | Numeric utilities, solvers, vector/matrix ops | `/src/core/math/` |
| **core-geometry** | Shapes, coordinate transforms, section geometry | `/src/core/geometry/` |
| **core-materials** | Steel, concrete, prestress property databases | `/src/core/materials/` |
| **core-units** | Unit conversion and enforcement | `/src/core/units/` |
| **core-validation** | Validation helpers, tolerance checks | `/src/core/validation/` |

Each of these is versioned and may be imported by domain modules (`beam-analysis`, `section-properties`, etc.).

---

# 3. Dependency Architecture (ASCII)

```
+-------------------------------+
|   Presentation / Applications |
+-------------------------------+
             |
             v
+-------------------------------+
|         Domain Modules        |
|  (beam, section, prestress)   |
+-------------------------------+
             |
             v
+-------------------------------+
|     Shared Core Libraries     |
| (math, geometry, materials…)  |
+-------------------------------+
             |
             v
+-------------------------------+
|     External Dependencies     |
|  (numpy, pyyaml, sqlite3)     |
+-------------------------------+
```

**Rule:** dependencies flow downward only.  Core libraries never import from domain or presentation layers.

---

# 4. Versioning & Release Policy

| Change Type | Examples | Action |
|--------------|-----------|---------|
| **Patch (X.Y.**z**)** | Minor bug fix, doc update, tolerance change | Auto-release after CI passes |
| **Minor (X.**y**.0)** | Backward-compatible feature addition | Requires validation + changelog |
| **Major (**x**.0.0)** | Breaking interface or algorithm change | Requires migration guide + formal review |

### Branch Model
```
main → stable release
dev  → integration & testing
feat/<lib-name> → new component
```

CI pipelines tag releases automatically (`v1.2.3`).

---

# 5. Packaging & Distribution

Each library is an **installable Python package** with `__init__.py` and `pyproject.toml`.

Example: `/src/core/math/pyproject.toml`
```toml
[project]
name = "core-math"
version = "1.0.0"
dependencies = ["numpy"]
```

For local development, link libraries via editable installs:
```bash
pip install -e src/core/math
```

Shared components can later be published to an internal index (e.g., `https://pypi.simplespan.local`).

---

# 6. Integration & Compatibility Testing

All shared libraries include:
1. **Unit tests** validating individual functions.  
2. **Integration tests** verifying cross-library behavior.  
3. **Validation tests** referencing CHBDC/CSA cases where applicable.  
4. **Compatibility matrix** stored in `/tests/integration/matrix.yaml`.

ASCII sketch:
```
[core-math] ─┬─> [core-geometry]
              ├─> [core-materials]
              └─> [core-units]
```
Each edge in the matrix must be validated by an integration test.

---

# 7. Database & Data Dependencies

If a shared library requires data (e.g., material properties):
- Provide defaults as **YAML** or **CSV** under `/data/materials/`.  
- For persistent datasets, support **SQLite** with schema defined in
  `/docs/framework/3-libraries/data-schema-and-interchange-standard.md`.
- Never hard-code file paths; use environment or config adapters.

Example SQLite schema:
```sql
CREATE TABLE materials (
  id TEXT PRIMARY KEY,
  name TEXT,
  type TEXT,
  fy_mpa REAL,
  fc_mpa REAL,
  density_kg_per_m3 REAL,
  reference TEXT
);
```

---

# 8. Validation & Certification

Each shared library maintains a **validation ledger**:

```
/docs/modules/<lib-name>/validation.md
```

Entry example:
```
ID: MAT-001
Test: Concrete f'c correlation
Reference: CSA A23.3-19 Clause 4.2
Result: PASS (tol = 1e-6)
```

All ledger entries must trace back to automated tests.

---

# 9. AI & Automation Integration

AI agents (Claude, Cursor) may:
- Propose boilerplate or refactors within shared libraries.  
- Generate docstrings & examples conforming to **Coding Standards**.  
- Update validation cases automatically if references change.

**Constraints:**
- AI cannot merge PRs.  
- Human review required for algorithmic or validation logic.  
- Agents must include metadata headers for all generated files.

---

# 10. ASCII Example — Library Integration Flow

```
(core-math) ---> provides numerical solvers
(core-geometry) ---> consumes math.solvers
(core-materials) ---> references material.db
(domain-beam) ---> imports from geometry, materials
(application-beam) ---> orchestrates domain-beam
```

---

# 11. Review Checklist

- [ ] Library versioned and documented  
- [ ] Downward-only dependencies  
- [ ] Tests and validation present  
- [ ] Changelog updated  
- [ ] AI contributions reviewed  
- [ ] Compatibility matrix updated  

---

# 12. References
- CHBDC CSA S6-19  
- CSA A23.3-19  
- CSA S16-19  
- *Clean Architecture* – R. Martin  
- *Software Engineering at Google* – T. Winters et al.
