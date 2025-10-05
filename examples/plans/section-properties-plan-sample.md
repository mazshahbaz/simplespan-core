---
title: Section Properties Module Plan (Sample)
version: 1.0
context: sections/properties
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# 🧭 YAML Resume Context

```yaml
resume_context:
  current_phase: 1
  last_ccp: vSEC-0-ccp-baseline
  progress_file: reports/progress.md
  key_docs:
    - docs/sections/section-properties-spec.md
    - validation/sections/seed-cases.json
```

# 📦 Scope
Define and deliver a reusable **Section Properties** capability with:
- **Standard shapes** (W, C, L, HSS, pipe per CSA/ASTM catalogs)  
- **Custom primitives** (rect, circle, polygon)  
- **Section builder** (union/holes/offsets, transformations)  
- **Cracked sections** and **with/without reinforcement** (user modifiers)  
- **Visualization** (ASCII/PNG), SI units, CHBDC-friendly outputs

---

## Phase 0 — Foundation ✅
_Set up scaffolding & seeds._

### ✅ Checklist
- [x] Create docs/sections/ and validation/sections/ folders
- [x] Add progress baseline entry
- [x] Add placeholder spec file and seed JSON

### Deliverables
- `docs/sections/section-properties-spec.md` (stub)
- `validation/sections/seed-cases.json`

---

## Phase 1 — Specification & Data Model
_Define entities, granularity, and SI conventions._

### ✅ Checklist
- [ ] Write spec: entities (Section, Shape, Material, Reinforcement, Transform)
- [ ] Define **granularity levels**: CatalogSection → BuiltSection → CrackedSection
- [ ] Specify properties set: A, Ix, Iy, Ixy, rx, ry, J, Cw, Sx, Sy, Zx, Zy, plastic mods
- [ ] Define **tolerances & units** (SI) and CHBDC clause references
- [ ] Draft section-builder ops (union, subtraction, holes, rotations, offsets)

### Deliverables
- `docs/sections/section-properties-spec.md`
- `docs/sections/section-builder-ops.md`

### Acceptance Criteria
- Spec references SI/metric; CHBDC citations by clause ID only
- Properties and symbols table agreed
- Examples: W250x33, HSS 152x152x6.4, Rect 300x500

---

## Phase 2 — Catalog & Custom Primitives
_Load catalog + implement primitives._

### ✅ Checklist
- [ ] Load CSA/ASTM-like catalog schema (no copyrighted tables; use placeholders)
- [ ] Implement primitives: rectangle, circle, polygon (CCW order, holes)
- [ ] Validate numerical seeds for A, Ix/Iy/Ixy vs hand calcs
- [ ] Support local axes, centroid, principal axes

### Deliverables
- `docs/sections/catalog-schema.md`
- `validation/sections/primitives.json`

### Acceptance Criteria
- Seed comparisons within tolerance (e.g., 1e-8 for area, 1e-6 for inertia)
- Unit tests planned for each shape

---

## Phase 3 — Section Builder & Transforms
_Compose complex sections from parts._

### ✅ Checklist
- [ ] Define composition JSON (parts, ops, transforms, material tags)
- [ ] Implement transforms: translate, rotate, mirror, offset (outer/inner)
- [ ] Implement Boolean ops: union, subtract (holes), intersect
- [ ] Validate centroid & inertia with parallel-axis checks

### Deliverables
- `docs/sections/section-builder-schema.md`
- `validation/sections/builder-cases.json`

### Acceptance Criteria
- Composition reproduced by independent calc within tolerance
- Edge cases: L-shape, T-shape, box-with-hole, multi-void polygon

---

## Phase 4 — Cracked & Reinforced Sections
_Analysis variations & modifiers._

### ✅ Checklist
- [ ] Define cracked section methodology (tension-stiffening option)
- [ ] Include reinforcement (bars/meshes) toggle; transformed-section option
- [ ] Allow user modifiers (λ for stiffness reduction; composite factors)
- [ ] Validation seeds for cracked inertia vs uncracked

### Deliverables
- `docs/sections/cracked-methods.md`
- `validation/sections/cracked-seeds.json`

### Acceptance Criteria
- Methods cite theory source (no copyrighted code text)
- Validation seeds pass configured tolerances

---

## Phase 5 — Visualization & Reporting
_Plots and tabular outputs._

### ✅ Checklist
- [ ] Define plotting requirements (section outline, centroid, principal axes)
- [ ] Define report schema (JSON + markdown tables)
- [ ] Station list formatting and unit annotations (SI)

### Deliverables
- `docs/sections/visualization-spec.md`
- `validation/sections/report-samples.json`

### Acceptance Criteria
- Plots render expected geometry/asymmetry indicators
- Reports are machine/human readable and SI-only

---

## Phase 6 — Packaging & Reuse
_Make it reusable across domains and agents._

### ✅ Checklist
- [ ] Define Python package boundary: `simplespan_sections`
- [ ] Document API surface (pure functions; deterministic)
- [ ] Add prompts & examples for AIC/agents to consume module

### Deliverables
- `docs/sections/api.md`
- `docs/framework/ai/prompts/sections-prompts.md`

### Acceptance Criteria
- API doc complete; deterministic expectations defined
- Example prompts produce consistent plans under AIC

---

*Prepared for SimpleSpan by Governance — 2025-10-05*
