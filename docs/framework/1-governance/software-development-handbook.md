---
title: Software Development Handbook
version: 1.0
context: framework/governance
last_reviewed: 2025-10-05
audience: structural_engineers, software_engineers, ai_agents
units: SI (metric)
codes: [CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19]
---

# 0. Purpose

This handbook defines **how we build, review, validate, release, and maintain** SimpleSpan Core — a Python structural engineering framework using **SI units** and aligned to **Canadian codes (CHBDC/CSA)**. It is optimized for collaboration with **AI coding agents** (Cursor, Claude).

**Core priorities (in order):**  
**Correctness → Clarity → Maintainability → Performance → Convenience.**

---

# 1. Principles

1. **Engineering correctness**  
   - Implement provisions as written; cite precise clauses (e.g., *CHBDC S6-19, 8.8.3*).  
   - Document assumptions, applicability limits, and references in code docstrings.

2. **Transparency & traceability**  
   - Every public function documents **units** and **references**.  
   - All features trace back to requirements; validation links to reference problems.

3. **Separation of concerns**  
   - Layering: **Presentation → Application → Domain → Infrastructure → Core**.  
   - Domain has **no UI** and depends only downward.

4. **Test-first mindset**  
   - Unit tests for logic; validation tests against code/examples; regression tests for bugs.

5. **SI units only (internal)**  
   - Convert at the boundaries (I/O, UI). Use MPa, kN, m, mm, °C.

---

# 2. Software Development Lifecycle (SDLC)

**2.1 Stages**
1. **Requirements** → capture features, inputs/outputs, references, tolerances.  
2. **Design** → module architecture, interfaces, data ownership, diagrams.  
3. **Implementation** → Python modules following Coding Standards.  
4. **Testing** → unit tests + integration tests; add validation cases.  
5. **Review** → peer review + AI-assisted review checklist.  
6. **Release** → version, changelog, tag; update docs.  
7. **Maintenance** → track issues, fix, add regression tests.

**2.2 Artifacts (per feature/module)**
- Requirements note (`/docs/modules/<module>/requirements.md`)  
- Design brief + interface spec (`/docs/modules/<module>/design.md`)  
- Code + docstrings (`/src/...`)  
- Tests (`/tests/unit/...`, `/tests/validation/...`)  
- Validation data (`/data/validation-cases/...`)  
- README examples and usage

---

# 3. Roles & Responsibilities

- **Structural Engineer (SE):** Owns correctness vs. code provisions; supplies references & validation cases.  
- **Software Engineer (SWE):** Owns architecture, code quality, testing infrastructure.  
- **Reviewer (SE/SWE):** Verifies implementation vs. provisions; signs off PR.  
- **AI Agent (Claude/Cursor):** Generates scaffolds, tests, and docs **under handbook rules**; cannot merge.  
- **Maintainer:** Approves releases, ensures Definition of Done.

---

# 4. Definition of Done (DoD)

A task/PR is **Done** only if:
- [ ] Requirements documented (inputs, outputs, units, references).  
- [ ] Code follows **Coding Standards** (naming, docstrings, exceptions).  
- [ ] **Tests:** unit + (if applicable) validation with tolerances.  
- [ ] **Docs updated:** module docs and user examples.  
- [ ] **CI passes:** lint, type (if enabled), tests, validation.  
- [ ] Reviewer approval.

---

# 5. Version Control & Branching

- Default branch: **main**.  
- Branch naming:  
  - `feat/<short-name>` new feature  
  - `fix/<short-name>` bug fix  
  - `docs/<short-name>` docs-only  
- Commit style: imperative, concise, reference issue when possible.  
- Use PRs for all changes; no direct commits to `main`.

---

# 6. Change Management

- Every PR links to an **issue** (bug/feature).  
- **Changelog** maintained in `CHANGELOG.md` (Keep a Changelog format).  
- Deprecations require: warning in code, docs notice, and migration note.

---

# 7. Units & Engineering Conventions

- **Internal calculations:** SI only (N, kN, m, mm, MPa, kN·m).  
- Function and variable names should carry unit clarity when ambiguous  
  (e.g., `stress_MPa`, `moment_kNm`, or documented in docstrings).  
- Materials and sections databases store SI with explicit metadata.

---

# 8. Documentation Policy

- **Location:** `/docs/framework` (governance/architecture/coding/validation), `/docs/modules/<module>`.  
- **Format:** Markdown with clear headings; include **YAML frontmatter** for AI agents.  
- **Content:** Purpose, responsibilities, interfaces, units, references, examples, validation links.  
- **Diagrams:** Store in `/docs/diagrams/` (C4/UML as needed).

---

# 9. Testing & Validation

- **Unit tests:** fast, isolated, deterministic; target ≥80% logic coverage in domain/core.  
- **Integration tests:** cross-module workflows.  
- **Validation tests:** compare against **CHBDC/CSA** or textbook references; keep inputs/expected outputs in `/data/validation-cases/`; define tolerances in `tolerances.yaml`.  
- **Regression tests:** each bug fix adds a test reproducing the issue.

---

# 10. CI/CD

- GitHub Actions: lint (ruff), tests (pytest), type checks (mypy optional), validation job.  
- All PRs must be green in CI.  
- Releases: tag `vX.Y.Z`, publish changelog, attach validation summary.

---

# 11. Security & Data

- Validate **all external inputs**; no silent failures.  
- No secrets in repo.  
- Large simulation outputs are not committed (use `/data/simulations/` in `.gitignore`).

---

# 12. AI Collaboration Rules (Claude/Cursor)

- Always provide the **module doc** and **framework docs** as context.  
- Ask AI to include:  
  - docstrings with units and references,  
  - input validation and typed exceptions,  
  - tests and examples.  
- Human reviews all AI changes; AI cannot approve or merge.  
- Prefer **small, reviewable PRs**.

---

# 13. References

- **CHBDC** CSA S6-19 — *Canadian Highway Bridge Design Code*  
- **CSA A23.3-19** — *Design of Concrete Structures*  
- **CSA S16-19** — *Design of Steel Structures*  
- Texts: *Mechanics of Materials*; *Reinforced Concrete Mechanics and Design*

---

# 14. Appendix — Templates

**PR checklist (paste into PR description):**
- [ ] Requirements documented with units & refs  
- [ ] Design/Interfaces updated  
- [ ] Tests (unit + validation) included  
- [ ] Docs updated  
- [ ] CI green

**Module doc sections:** Overview · Responsibilities · Interfaces (I/O + units) · Dependencies · Algorithms (refs) · Validation · Examples · Changelog
