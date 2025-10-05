---
title: Coding & Implementation Standards (Python)
version: 1.0
context: framework/coding
last_reviewed: 2025-10-05
audience: structural_engineers, software_engineers, ai_agents
units: SI (metric)
codes: [CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19]
---

© 2025 SimpleSpan Software. All rights reserved.

# 0. Purpose
Define **Python coding standards** for SimpleSpan Core with **SI units**, **CHBDC/CSA** references, and **AI-collaboration** rules.

# 1. Python Baseline
- Python **3.11+**.
- Style: **PEP 8** + project specifics below.
- Tooling: **ruff** (lint), **pytest** (tests), **mypy** optional (types).

# 2. Naming & Structure
- **Packages/Modules:** `snake_case` — `section_properties`, `beam_analysis`.
- **Classes:** `PascalCase` — `SectionPropertiesCalculator` (use sparingly; prefer functions).
- **Functions/Variables:** `snake_case` — `compute_centroid`, `stress_mpa`.
- **Constants:** `UPPER_SNAKE_CASE` — `MAX_ITER`, `DEFAULT_TOL`.
- **Private/Internal:** prefix `_` — `_check_polygon_winding`.

**Units in Names (when ambiguous):**
- Prefer clarity: `moment_kNm`, `stress_mpa`, `length_mm`. Otherwise document units in docstring.

# 3. Docstrings & References
Use Google or NumPy style. **Always specify units** and **references**.

```python
def flexural_capacity_m_kNm(fc_mpa: float, fy_mpa: float, b_mm: float, d_mm: float) -> float:
    """Compute factored flexural capacity (φMn) in **kN·m**.
    Args:
      fc_mpa: Concrete compressive strength (MPa).
      fy_mpa: Steel yield strength (MPa).
      b_mm: Section width (mm).
      d_mm: Effective depth (mm).
    Returns:
      Factored moment capacity (kN·m).
    References:
      CSA A23.3-19 Clause 10.x; CHBDC S6-19 as applicable.
    Raises:
      ValueError: If inputs are non-positive or outside typical ranges.
    """
```

# 4. Exceptions & Messages
- Validate all public inputs; raise `ValueError`, `TypeError`, or domain-specific exceptions.
- Messages must be **actionable**: include parameter name, value, expected range/units.

# 5. Imports & Dependencies
- Absolute imports within package; **no cross-layer upward imports**.
- Standard library preferred; keep dependencies minimal and vetted.

# 6. Units Policy (Mandatory)
- **SI internally**. Convert only at boundary layers.
- Provide converter helpers in `core/units/` for common patterns.

```python
def kN_to_N(x_kN: float) -> float: return x_kN * 1_000.0
def mm_to_m(x_mm: float) -> float: return x_mm / 1_000.0
```

# 7. File/Folder Organization
```
src/
  simplespan_core/           # package root
  core/                      # math, geometry, materials, units
  domain/                    # engineering modules
tests/
  unit/                      # test_<module>.py
  validation/                # reference cases
docs/
  framework/                 # standards
```

# 8. Testing Standards
- **Unit tests** for each function/class (edge cases too).
- Use numeric **tolerances** for floats (e.g., `abs(a-b) <= 1e-9` or % tolerance).
- **Validation tests** must cite source and store expected values.

Example:
```python
import math

def almost_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
```

# 9. Performance & Precision
- Prefer clarity; optimize after profiling.
- Avoid unnecessary copies; prefer vectorization if justified.
- Document any approximations or numerical techniques used.

# 10. Code Review Checklist
- [ ] Docstrings include **units** and **references**
- [ ] Input validation + precise exceptions
- [ ] No upward-layer imports
- [ ] Tests cover edge cases + happy path
- [ ] Numeric tolerances justified
- [ ] Names readable and unit-clear

# 11. AI Collaboration
Prompts should request: **docstrings with units**, **input validation**, **tests**, and **references**.
AI-generated code must pass **lint + tests** and be **human-reviewed**.

# 12. Examples (Mini)
```python
def compute_uniform_load_max_moment_kNm(w_kN_per_m: float, L_m: float) -> float:
    """Max M for simply supported beam under uniform load: wL^2/8 (kN·m).
    Args:
      w_kN_per_m: Uniform load (kN/m).
      L_m: Span length (m).
    Returns:
      Maximum bending moment (kN·m).
    References:
      Mechanics of Materials; CHBDC S6-19 basic load effects.
    """
    if w_kN_per_m < 0 or L_m <= 0:
        raise ValueError(f"w ({w_kN_per_m} kN/m) must be >= 0 and L ({L_m} m) > 0.")
    return w_kN_per_m * (L_m ** 2) / 8.0
```

# 13. References
- CHBDC CSA S6-19; CSA A23.3-19; CSA S16-19.