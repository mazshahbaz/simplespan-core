---
title: ADR-002 — Five-Layer Architecture and Dependency Rules
version: 1.0
context: governance/adrs
last_reviewed: 2025-10-05
status: Accepted
decision_date: 2025-10-05
---

# ADR-002: Five-Layer Architecture and Dependency Rules

## Status
**Accepted** — 2025-10-05

## Context
Software architectures need clear boundaries to remain maintainable, testable, and extensible. Without explicit layering, dependencies become circular, testing becomes difficult, and domain logic gets polluted with UI or infrastructure concerns.

SimpleSpan requires a structure that:
- Isolates engineering calculations (domain) from UI/IO
- Supports testing without external dependencies
- Enables AI agents to understand module boundaries
- Scales to multiple structural engineering domains

## Decision
**Implement a strict five-layer architecture with one-way dependencies.**

### Layer Hierarchy (Top to Bottom):
```
Presentation    → UI, API, CLI
     ↓
Application     → Orchestration, workflows, use cases
     ↓
Domain          → Engineering calculations (section-properties, beam-analysis, FEA)
     ↓
Infrastructure  → IO, persistence, logging, config, rendering
     ↓
Core            → Math, geometry, materials, units, validation utilities
```

### Dependency Rules:
1. **One-way only**: Layers may depend ONLY on layers below them
2. **No upward imports**: Domain cannot import Application or Presentation
3. **No skip dependencies**: Prefer importing from adjacent layer
4. **Infrastructure isolation**: Domain is pure logic; Infrastructure handles side effects

### Repository Mapping:
```
src/
├── presentation/      # CLI, web, desktop UI
├── application/       # beam-app, section-app, orchestration
├── domain/            # section-properties, beam-analysis, prestressing
├── infrastructure/    # data-access, io, config, logging, rendering
└── core/              # math, geometry, materials, units, validation
```

## Rationale
1. **Testability**: Domain logic can be tested without UI or database
2. **Maintainability**: Clear boundaries make changes predictable
3. **Reusability**: Core and domain layers can be used by multiple applications
4. **AI-Friendly**: Agents can understand module scope and dependencies
5. **Separation of Concerns**: Engineering logic separate from technical infrastructure

## Consequences

### Positive:
- Pure domain logic (no side effects)
- Fast unit tests (no IO dependencies)
- Clear module boundaries for AI planning
- Easy to add new presentation layers (CLI, Web, API)
- Infrastructure changes don't affect domain calculations

### Negative:
- More files and indirection
- Must pass data through layers explicitly
- Learning curve for developers unfamiliar with layered architecture

### Mitigations:
- Provide architecture diagrams and examples
- Use consistent patterns for layer interaction
- Document layer responsibilities clearly
- AI router enforces dependency rules during code generation

## Implementation Guidelines

### Core Layer:
- No external dependencies (except standard library, numpy, scipy)
- Pure functions preferred
- No logging (return errors explicitly)
- Examples: `math/solvers.py`, `geometry/shapes.py`, `units/conversions.py`

### Infrastructure Layer:
- Adapts external systems (files, databases, plotting)
- Implements interfaces defined by domain
- Handles I/O, logging, config
- Examples: `io/section_loader.py`, `rendering/plot_section.py`

### Domain Layer:
- Engineering calculations and business rules
- SI units internally (ADR-001)
- Typed interfaces and validation
- Examples: `section_properties/calculator.py`, `beam_analysis/shear_moment.py`

### Application Layer:
- Coordinates domain modules
- Implements use cases and workflows
- No calculation logic
- Examples: `beam_app/analyze_beam.py`, `section_app/section_builder.py`

### Presentation Layer:
- User interfaces (CLI, web, desktop)
- Input validation and formatting
- Unit conversions for display
- Examples: `cli/beam_cli.py`, `web/api_server.py`

## Validation
- Code reviews check for upward dependencies
- Import analysis tools can detect violations
- CI can enforce layer dependencies via import checking

## Related Decisions
- ADR-001: SI Units (domain uses SI internally)
- ADR-004: Domain Granularity (defines domain module boundaries)

## References
- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- Hexagonal Architecture (Alistair Cockburn)
