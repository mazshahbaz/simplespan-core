---
title: Software Development Handbook
version: 1.0
brand: SimpleSpan Software
repo: simplespan-core
context: framework/governance
audience: structural_engineers, software_engineers, ai_agents
units: SI (metric)
codes: [CHBDC CSA-S6:19, CSA A23.3:19, CSA S16:19]
related:
  - ../1-governance/software-architecture-guide.md
  - ../1-governance/coding-implementation-standards.md
  - ../2-validation/validation-verification-manual.md
---

# 0. Purpose
This handbook defines **how we build, review, validate, release, and maintain** SimpleSpan Core — a Python structural engineering framework using **SI units** and aligned to **Canadian codes (CHBDC/CSA)**. It is optimized for collaboration with **AI coding agents** (Cursor, Claude).

**Core priorities (in order):**  
**Correctness → Clarity → Maintainability → Performance → Convenience.**

# 1. Principles
1. **Engineering correctness** — Implement provisions as written; cite precise clauses (e.g., *CHBDC S6-19, 8.8.3*).  
2. **Transparency & traceability** — Docstrings include **units** and **references**.  
3. **Separation of concerns** — **Presentation → Application → Domain → Infrastructure → Core**.  
4. **Test-first mindset** — Unit + validation + regression tests.  
5. **SI units only (internal)** — Convert only at boundaries.

# 2. SDLC
1) Requirements → 2) Design → 3) Implementation → 4) Testing → 5) Review → 6) Release → 7) Maintenance  
Artifacts per module: requirements, design/interface spec, code+docstrings, tests, validation data, examples.

# 3. Roles & Responsibilities
SE, SWE, Reviewer, AI Agent (assist only, no merges), Maintainer.

# 4. Definition of Done (DoD)
- [ ] Requirements w/ units & refs  
- [ ] Coding Standards followed  
- [ ] Unit + validation tests  
- [ ] Docs updated  
- [ ] CI green  
- [ ] Reviewer approval

# 5. Git & Branching
main default. Branches: eat/*, ix/*, docs/*. PRs only, no direct commits to main.

# 6. Change Management
Issues link to PRs; maintain CHANGELOG.md; deprecations include warnings & migration notes.

# 7. Units & Conventions
SI internal (N, kN, m, mm, MPa, kN·m). Clarify units in names or docstrings (stress_MPa, moment_kNm).

# 8. Documentation
Markdown + YAML frontmatter. Locations: /docs/framework and /docs/modules/<module>. Diagrams in /docs/diagrams/.

# 9. Testing & Validation
Unit, integration, validation (CHBDC/CSA refs; data under /data/validation-cases/; tolerances in 	olerances.yaml), regression.

# 10. CI/CD
GitHub Actions: ruff, pytest, (mypy opt.), validation job. Releases: tag X.Y.Z, changelog, validation summary.

# 11. Security & Data
Validate all external inputs; no secrets in repo; large outputs ignored via .gitignore.

# 12. AI Collaboration Rules
Provide module+framework docs as context; require docstrings (units+refs), validation & tests; human review & small PRs.

# 13. References
CHBDC CSA S6-19; CSA A23.3-19; CSA S16-19; standard texts.

# 14. Appendix
PR Checklist and module doc sections template.
