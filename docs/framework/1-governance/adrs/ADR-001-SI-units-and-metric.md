---
title: ADR-001 — SI Units and Metric System
version: 1.0
context: governance/adrs
last_reviewed: 2025-10-05
status: Accepted
decision_date: 2025-10-05
---

# ADR-001: SI Units and Metric System

## Status
**Accepted** — 2025-10-05

## Context
Structural engineering software must handle physical quantities (forces, lengths, stresses, moments) with consistent units to prevent calculation errors. Different regions use different unit systems (Imperial vs. Metric), and inconsistent internal representation leads to bugs and validation failures.

The SimpleSpan framework targets Canadian codes (CHBDC, CSA) which primarily use metric units, though some legacy standards include imperial references.

## Decision
**All internal calculations and data structures use SI (metric) units exclusively.**

### Specific Conventions:
- **Force**: N, kN (Newtons, kilonewtons)
- **Length**: m, mm (meters, millimeters)
- **Stress**: MPa, Pa (megapascals, pascals)
- **Moment**: kN·m (kilonewton-meters)
- **Mass**: kg (kilograms)
- **Temperature**: °C (Celsius)
- **Angle**: radians (rad) for calculations, degrees (°) for display only

### Implementation Rules:
1. **Internal**: All domain logic, core libraries, and data storage use SI units
2. **Boundaries**: Unit conversion occurs ONLY at presentation/infrastructure boundaries
3. **Variable Naming**: When ambiguous, include units in variable names (e.g., `moment_kNm`, `length_mm`)
4. **Documentation**: All docstrings must explicitly state units for physical quantities
5. **Validation**: Test cases and reference data use SI units with explicit labels

## Rationale
1. **Code Alignment**: CHBDC and CSA standards primarily specify SI units
2. **Consistency**: Single internal representation eliminates conversion errors
3. **Simplicity**: Domain logic never worries about unit conversions
4. **Auditability**: Clear, traceable calculations for engineering review
5. **International**: SI is the global standard for scientific computation

## Consequences

### Positive:
- Eliminates entire class of unit conversion bugs
- Simplifies domain logic (no conversion handling)
- Aligns with Canadian code requirements
- Facilitates validation against CHBDC/CSA examples
- Clear separation of concerns (domain vs. presentation)

### Negative:
- Users working in imperial units need conversions at UI layer
- Some legacy reference materials use imperial units
- Must maintain conversion utilities for I/O boundaries

### Mitigations:
- Provide `core/units/` module with vetted conversion functions
- Document conversion policy clearly in architecture guide
- Test conversions with known reference values
- Support imperial display units at presentation layer only

## Compliance
- All new code must follow this standard
- Variable names with physical quantities should indicate units when ambiguous
- Code reviews must verify SI unit usage
- Validation tests must use SI reference values

## Related Decisions
- ADR-002: Layer Architecture (defines where conversions occur)
- ADR-004: Domain Granularity (domain modules use SI internally)

## References
- CHBDC CSA S6-19 (uses metric units)
- CSA A23.3-19 (uses metric units)
- CSA S16-19 (uses metric units)
- ISO 1000:1992 — SI units and recommendations
