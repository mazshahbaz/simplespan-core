---
title: Validation & Verification Manual
version: 1.0
context: framework/validation
last_reviewed: 2025-10-05
audience: structural_engineers, software_engineers, qa, auditors, ai_agents
units: SI (metric)
codes: [CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19]
---

© 2025 SimpleSpan Software. All rights reserved.

# 0. Purpose
Define the **end-to-end V&V process** for SimpleSpan Core to ensure computational **correctness, traceability, and auditability** against **CHBDC/CSA** and accepted references.

# 1. Vocabulary
- **Verification:** Did we build it right? (code vs. spec)
- **Validation:** Did we build the right thing? (results vs. references)
- **Benchmark Case:** A test with known reference values (from code, textbook, or analytical solution).

# 2. V&V Process (ASCII Overview)

```
[Requirements] --> [Design] --> [Implementation] --> [Verification Tests]
                                           |
                                           v
                                     [Validation]
                                      (CHBDC/CSA)
                                           |
                                           v
                                      [Reporting]
```

# 3. Test Taxonomy
1. **Unit Tests:** Function-level checks; deterministic and fast.
2. **Integration Tests:** Multi-module workflows.
3. **Validation Tests:** Compare outputs to authoritative references.
4. **Regression Tests:** Reproduce fixed bugs; locked forever.

# 4. Validation Case Structure
- **Location:** `/tests/validation/<module>/cases/`
- **Data File:** JSON (`.json`) with SI units:
```json
{
  "id": "SPN-001",
  "title": "Rectangular section properties",
  "inputs": { "b_mm": 300.0, "h_mm": 600.0 },
  "expected": { "area_mm2": 180000.0, "Iy_mm4": 3.24e9, "Iz_mm4": 8.1e8 },
  "tolerances": { "relative": 1e-6, "absolute": 1e-9 },
  "reference": "Mechanics of Materials, Example X.Y"
}
```
- **Test Code:** loads JSON, runs module, asserts within tolerance.

# 5. Tolerances & Precision
- Define global defaults in `tests/validation/tolerances.yaml`:
```
defaults:
  relative: 1e-6
  absolute: 1e-9
module_overrides:
  section-properties:
    relative: 1e-7
```
- Choose **relative** tolerance for scale-free comparisons; add **absolute** for near-zero results.

# 6. Source Hierarchy (for References)
1. **CHBDC / CSA clauses** and official examples where applicable.
2. **Peer-reviewed textbooks** and reputable publications.
3. **Analytical solutions** (closed-form).
4. **Cross-checked numerical results** from independent tools.

# 7. Validation Workflow (ASCII)
```
[Select Case] -> [Create JSON Inputs/Expected] -> [Implement Test]
       |                   |                               |
       v                   v                               v
  [Cite Clause]     [Define Tolerances]             [Run in CI/CD]
       \__________  _______________________________/
                  \/
          [Review & Approve Validation Case]
```

# 8. Reporting & Traceability
- Each validation test prints: case id, reference, tolerance, pass/fail.
- Keep a **Validation Index** in `/docs/modules/<module>/validation.md`.
- Releases append a **Validation Summary** to `CHANGELOG.md`.

# 9. CI Integration
- GitHub Actions job runs `pytest -m validation` on PRs and main.
- Artifacts: JSON logs of validation runs for audit.

# 10. Nonconformance Handling
- If **discrepancy > tolerance**:
  1) Mark test failed; 2) open issue; 3) root-cause analysis; 4) fix; 5) add regression test.

# 11. Example Validation Test (Sketch)
```python
import json, pathlib
from simplespan_core.domain.section_properties import compute_section_properties

def test_rect_section_properties_validation():
    case = json.loads(pathlib.Path(__file__).with_name("rect.json").read_text())
    res = compute_section_properties([(0,0), (300,0), (300,600), (0,600)])
    assert abs(res["area_mm2"] - case["expected"]["area_mm2"]) <= case["tolerances"]["absolute"]
```

# 12. Review Checklist (Validation)
- [ ] Case has authoritative reference
- [ ] Inputs/outputs in **SI**
- [ ] Tolerances justified
- [ ] Test automated in CI
- [ ] Results documented in module validation index

# 13. References
- CHBDC CSA S6-19; CSA A23.3-19; CSA S16-19.
- *Mechanics of Materials*; other reputable texts.