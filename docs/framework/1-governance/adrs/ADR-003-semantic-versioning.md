---
title: ADR-003 — Semantic Versioning for SimpleSpan
version: 1.0
context: governance/adrs
last_reviewed: 2025-10-05
status: Accepted
decision_date: 2025-10-05
---

# ADR-003: Semantic Versioning for SimpleSpan

## Status
**Accepted** — 2025-10-05

## Context
Engineering software requires predictable versioning to ensure:
- Users know when breaking changes occur
- Validation results remain reproducible
- Dependencies can specify compatible version ranges
- CCPs (Continuity Checkpoints) can reference specific releases

Without a versioning standard, users cannot trust that updates won't break their workflows or change calculation results.

## Decision
**Use Semantic Versioning (SemVer) 2.0.0 for all SimpleSpan releases.**

### Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes or calculation methodology changes
- **MINOR**: Backward-compatible new features
- **PATCH**: Backward-compatible bug fixes

### Version Increment Rules:

#### MAJOR version increment when:
- Breaking API changes (function signatures, parameter meanings)
- Calculation methodology changes that alter results
- Removal of public functions or modules
- Changes to validated calculation outputs
- Schema changes that break existing data files

#### MINOR version increment when:
- Adding new modules or functions (backward-compatible)
- New features that don't change existing outputs
- Performance improvements without result changes
- New validation test cases
- Documentation improvements (significant)

#### PATCH version increment when:
- Bug fixes that restore correct behavior
- Documentation corrections
- Internal refactoring without external impact
- Performance fixes without result changes
- Test improvements

### Pre-release Versions:
- Format: `MAJOR.MINOR.PATCH-alpha.N`, `-beta.N`, `-rc.N`
- Used for development and testing
- Not for production engineering calculations

### Build Metadata:
- Format: `MAJOR.MINOR.PATCH+build.timestamp`
- Optional for internal tracking
- Does not affect version precedence

## Rationale
1. **Industry Standard**: SemVer is widely understood and tooling-supported
2. **Predictability**: Users know when updates are safe to apply
3. **Reproducibility**: Version pins ensure identical calculation results
4. **Dependency Management**: Python packaging supports SemVer ranges
5. **Auditability**: CCP tags reference specific semantic versions

## Consequences

### Positive:
- Clear communication of change impact
- Safe automatic updates for PATCH and MINOR (with testing)
- Validation reproducibility with version pinning
- Professional release management
- CCP tracking aligned with versions

### Negative:
- Must maintain backward compatibility for MINOR releases
- MAJOR releases require migration guides
- Stricter discipline on what constitutes a breaking change

### Mitigations:
- Document breaking changes clearly in CHANGELOG
- Provide migration guides for MAJOR releases
- Deprecation warnings before removing features
- Maintain compatibility for at least one MAJOR version

## Implementation Guidelines

### Version Declaration:
- `pyproject.toml`: Single source of truth
- `src/simplespan_core/__version__.py`: Programmatic access
- Git tags: `vMAJOR.MINOR.PATCH`

### CHANGELOG:
- Keep a Changelog format (keepachangelog.com)
- Sections: Added, Changed, Deprecated, Removed, Fixed, Security
- Link each version to release notes and CCP

### Calculation Changes:
- Any change to engineering calculations increments MAJOR
- Exception: Bug fixes that restore code-compliant behavior (PATCH)
- Document expected vs. actual behavior in release notes

### API Stability:
- Public API: Any function/class in top-level `__init__.py`
- Internal API: Prefixed with `_`, can change in MINOR releases
- Experimental API: Marked with decorator, can change in MINOR releases

### Validation Versioning:
- Validation test suites versioned with framework
- Test case IDs reference version where introduced
- Expected results locked per version

## Version Zero (0.x.x):
- `0.x.x` indicates pre-stable development
- Breaking changes allowed in MINOR increments
- Move to `1.0.0` when API and calculations are production-ready

## CCP Integration:
- Each CCP tag references a semantic version
- Format: `vMAJOR.MINOR.PATCH-ccp-<phase>-<slug>`
- Example: `v1.2.0-ccp-phase-1-governance`

## Related Decisions
- ADR-007: Change Management (when to increment versions)
- CCP Policy (version tagging and continuity)

## References
- Semantic Versioning 2.0.0: https://semver.org/
- Keep a Changelog: https://keepachangelog.com/
- PEP 440 (Python versioning): https://peps.python.org/pep-0440/
