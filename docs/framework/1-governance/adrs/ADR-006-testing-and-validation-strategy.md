---
title: ADR-006 — Testing and Validation Strategy
version: 1.0
context: governance/adrs
last_reviewed: 2025-10-05
status: Accepted
decision_date: 2025-10-05
---

# ADR-006: Testing and Validation Strategy

## Status
**Accepted** — 2025-10-05

## Context
Structural engineering software produces calculations that directly impact safety. Unlike typical software, incorrect results can lead to structural failures. We need a testing strategy that:
- Verifies code correctness against engineering standards
- Validates outputs against known reference solutions
- Enables regression testing when bugs are fixed
- Supports AI-generated code validation
- Provides audit trail for professional accountability

## Decision
**Implement a four-tier testing strategy with explicit validation against CHBDC/CSA references.**

### Testing Tiers:

#### Tier 1: Unit Tests
**Purpose**: Verify individual functions and methods

- **Scope**: Single function or class
- **Speed**: Fast (milliseconds per test)
- **Dependencies**: None (pure functions preferred)
- **Coverage Target**: ≥80% for core and domain layers
- **Location**: `tests/unit/<module>/test_*.py`

**Characteristics**:
- Deterministic (same inputs → same outputs)
- Test edge cases and error handling
- Use numeric tolerances for floating-point comparisons
- No I/O or external dependencies

**Example**:
```python
def test_rectangle_area():
    area = compute_rectangle_area(b_mm=300.0, h_mm=500.0)
    expected = 150000.0  # mm²
    assert abs(area - expected) < 1e-6
```

#### Tier 2: Integration Tests
**Purpose**: Verify multi-module workflows

- **Scope**: Cross-module interactions
- **Speed**: Moderate (seconds per test)
- **Dependencies**: Multiple domain modules
- **Coverage Target**: Key workflows covered
- **Location**: `tests/integration/test_*.py`

**Characteristics**:
- Test realistic engineering workflows
- Verify data flow between modules
- Check interface compatibility
- May include infrastructure (file I/O)

**Example**:
```python
def test_beam_analysis_with_section_properties():
    section = load_section_properties("W250x33")
    beam = create_simple_beam(section, span_m=6.0)
    results = analyze_beam(beam, load_kN_m=10.0)
    assert results.max_moment_kNm > 0
```

#### Tier 3: Validation Tests
**Purpose**: Verify correctness against CHBDC/CSA and reference solutions

- **Scope**: Complete calculations vs. known answers
- **Speed**: Moderate to slow
- **Dependencies**: May include data files
- **Coverage Target**: All major calculation paths
- **Location**: `tests/validation/<module>/test_*.py`
- **Data**: `tests/validation/<module>/cases/*.json`

**Characteristics**:
- Compare outputs to CHBDC/CSA worked examples
- Use textbook problems with known solutions
- Include reference source and clause numbers
- Define explicit tolerances (relative and absolute)
- Store expected values in JSON files

**JSON Format**:
```json
{
  "id": "SPN-001",
  "title": "Rectangular section properties",
  "reference": "CHBDC Commentary Example 5.2",
  "inputs": {
    "b_mm": 300.0,
    "h_mm": 600.0
  },
  "expected": {
    "area_mm2": 180000.0,
    "Ix_mm4": 5.4e9,
    "Iy_mm4": 1.35e9
  },
  "tolerances": {
    "relative": 1e-6,
    "absolute": 1e-9
  }
}
```

**Test Implementation**:
```python
def test_validation_SPN_001():
    case = load_validation_case("SPN-001")
    section = RectangularSection(**case["inputs"])
    props = section.compute_properties()

    for key, expected in case["expected"].items():
        actual = getattr(props, key)
        assert_within_tolerance(actual, expected, case["tolerances"])
```

#### Tier 4: Regression Tests
**Purpose**: Prevent bugs from reappearing

- **Scope**: Previously discovered bugs
- **Speed**: Fast to moderate
- **Dependencies**: Minimal
- **Coverage Target**: One test per fixed bug
- **Location**: `tests/regression/test_issue_*.py`

**Characteristics**:
- Named after GitHub issue number
- Include minimal reproduction case
- Locked forever (never removed)
- Document what bug was fixed

**Example**:
```python
def test_issue_42_negative_area_with_holes():
    """Regression test for issue #42: holes subtracted twice"""
    section = CompositeSection(...)
    section.add_hole(...)
    area = section.compute_area()
    assert area > 0  # Was negative before fix
```

## Tolerance Strategy

### Default Tolerances:
Defined in `tests/validation/tolerances.yaml`:
```yaml
defaults:
  relative: 1e-6   # 0.0001% relative error
  absolute: 1e-9   # Absolute error for near-zero values

module_overrides:
  section-properties:
    relative: 1e-7
  beam-analysis:
    relative: 1e-5   # Iterative methods may need looser tolerance
```

### Tolerance Selection:
- **Relative tolerance**: For scale-independent comparisons
- **Absolute tolerance**: For values near zero
- **Combined**: `|actual - expected| ≤ max(abs_tol, rel_tol * |expected|)`

## Reference Hierarchy (for Validation):
1. **Primary**: CHBDC/CSA official worked examples
2. **Secondary**: Peer-reviewed textbooks (Salmon & Johnson, MacGregor, etc.)
3. **Tertiary**: Analytical solutions (closed-form equations)
4. **Quaternary**: Cross-checked numerical results (multiple independent tools)

## Test Automation

### CI Requirements:
- All PRs must pass **all** test tiers
- Coverage reports generated and tracked
- Validation tests run on every commit
- Regression tests never skipped

### Test Commands:
```bash
# Run all tests
pytest -q

# Run specific tier
pytest tests/unit/
pytest tests/validation/

# Run with coverage
pytest --cov=simplespan_core

# Run single module
pytest tests/unit/section_properties/
```

## AI-Generated Code Requirements:
All AI-generated code must include:
- Unit tests for new functions
- Validation tests if implementing CHBDC/CSA calculations
- Test docstrings explaining what is tested
- References to validation sources

## Rationale
1. **Safety**: Engineering calculations must be verifiable
2. **Traceability**: Tests document calculation intent
3. **Auditability**: Validation cases provide audit trail
4. **Regression Prevention**: Fixed bugs stay fixed
5. **AI Validation**: Tests verify AI-generated code
6. **Professional Standard**: Meets engineering software QA expectations

## Consequences

### Positive:
- High confidence in calculation correctness
- Clear audit trail for engineering review
- Regression prevention
- AI outputs automatically validated
- Professional-grade software quality

### Negative:
- Upfront effort to create validation cases
- Must maintain reference data files
- Test suite execution time increases
- Requires access to CHBDC/CSA worked examples

### Mitigations:
- Start with critical paths, expand coverage over time
- Use test fixtures to reduce duplication
- Parallelize test execution in CI
- Create validation cases incrementally with each module

## Validation Evidence Pack:
For each module, maintain:
- `/docs/modules/<module>/validation.md` — Test strategy
- `/tests/validation/<module>/cases/*.json` — Test cases
- `/tests/validation/<module>/references/` — Source PDFs/images
- `/reports/validation/<module>-report.html` — Test results summary

## Related Decisions
- ADR-001: SI Units (all test data uses SI)
- ADR-004: Domain Granularity (tests organized by module)
- ADR-005: AI Governance (AI must generate tests)

## References
- `docs/framework/2-validation/validation-verification-manual.md`
- IEEE 1012-2016 (Software Verification and Validation)
- ISO 9001 Quality Management
- CHBDC CSA S6-19 Commentary (worked examples)
