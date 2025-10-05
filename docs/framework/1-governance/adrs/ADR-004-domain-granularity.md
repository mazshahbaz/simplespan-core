---
title: ADR-004 — Domain Module Granularity
version: 1.0
context: governance/adrs
last_reviewed: 2025-10-05
status: Accepted
decision_date: 2025-10-05
---

# ADR-004: Domain Module Granularity

## Status
**Accepted** — 2025-10-05

## Context
Structural engineering encompasses many calculation domains: section properties, beam analysis, FEA, material behavior, prestressing, connections, foundations, etc. Poor module boundaries lead to:
- Monolithic modules that are hard to test
- Circular dependencies
- Difficult AI-assisted development (agents confused about scope)
- Unclear ownership and validation responsibility

We need clear principles for when to create a new domain module vs. extending an existing one.

## Decision
**Define domain modules by engineering calculation responsibility, following these granularity principles:**

### Module Definition Criteria:
A domain module is created when it has:
1. **Distinct engineering purpose** (e.g., "compute section properties" vs. "analyze beams")
2. **Independent inputs/outputs** (can be validated separately)
3. **Clear code reference** (maps to specific CHBDC/CSA chapters)
4. **Manageable scope** (≤2000 LOC for core calculations)
5. **Stable interface** (inputs/outputs unlikely to change)

### Core Domain Modules (Initial Set):
```
domain/
├── section-properties/    # Geometric section analysis (A, I, S, Z, r)
├── beam-analysis/         # Shear, moment, deflection (simple beams)
├── materials/             # Material properties (steel, concrete, prestress)
├── prestressing/          # Prestress losses, effective force
├── cracked-section/       # Transformed sections, neutral axis
├── moment-curvature/      # M-φ analysis for ductility
└── connections/           # (future) Bolt, weld, bearing design
```

### Granularity Rules:

#### Too Coarse (avoid):
- ❌ `structural-analysis/` — too broad, combines unrelated calculations
- ❌ `concrete/` — mixes materials, sections, and design checks

#### Too Fine (avoid):
- ❌ `centroid/` — too small, belongs in `section-properties`
- ❌ `moment-of-inertia/` — too small, part of `section-properties`

#### Just Right:
- ✅ `section-properties/` — focused, clear validation, stable interface
- ✅ `beam-analysis/` — distinct from FEA, clear code mapping
- ✅ `prestressing/` — complex enough for own module, clear code reference

## Rationale
1. **Testability**: Small modules with clear interfaces are easier to validate
2. **AI Planning**: Agents can plan implementation within module boundaries
3. **Code Mapping**: Each module maps to specific CHBDC/CSA sections
4. **Parallel Development**: Multiple modules can be developed simultaneously
5. **Validation Clarity**: Test cases organized by module responsibility

## Consequences

### Positive:
- Clear validation boundaries (test section-properties independently)
- AI agents can plan modules end-to-end
- Easy to assign ownership (structural engineer per module)
- Natural organization for documentation
- Modules can version independently if needed

### Negative:
- More directories and initial scaffolding
- Must coordinate interfaces between related modules
- Risk of creating too many small modules

### Mitigations:
- Start with core set (6-8 modules)
- Merge modules if interface coordination becomes complex
- Use shared `core/` libraries for common utilities
- Document inter-module dependencies explicitly

## Module Structure Template:
```
domain/<module-name>/
├── __init__.py
├── <module_name>.py        # Main calculations
├── interfaces.py           # Typed public API
├── algorithms.py           # Core calculation functions
├── validators.py           # Input validation
└── README.md               # Module overview

docs/modules/<module-name>/
├── overview.md             # Purpose, scope, assumptions
├── interfaces.md           # API documentation
├── algorithms.md           # Method details with CHBDC/CSA references
├── validation.md           # Test cases and references
└── changelog.md            # Module version history

tests/unit/<module-name>/
tests/validation/<module-name>/cases/*.json
```

## Inter-Module Dependencies

### Allowed:
- `beam-analysis` → `section-properties` (needs I, S, Z)
- `cracked-section` → `materials` (needs E, f'c, fy)
- `prestressing` → `materials` (needs tendon properties)

### Prohibited:
- Circular dependencies
- Upward dependencies (domain → application)
- Cross-domain without clear interface

## Module Lifecycle:

### Planning Phase:
1. Create module plan using `plan_module.prompt.md`
2. Define interfaces, inputs, outputs, units
3. Identify validation cases and references
4. Document dependencies

### Implementation Phase:
5. Scaffold module structure
6. Implement algorithms with CHBDC/CSA citations
7. Write unit and validation tests
8. Document API and examples

### Maintenance Phase:
9. Version module with framework
10. Track changes in module changelog
11. Maintain backward compatibility (ADR-003)

## Related Decisions
- ADR-002: Layer Architecture (domain layer defined)
- ADR-001: SI Units (all domain modules use SI)
- ADR-005: AI Governance Integration (modules planned with AI Router)

## References
- Domain-Driven Design (bounded contexts)
- Clean Architecture (use case granularity)
- SimpleSpan module planning playbook
