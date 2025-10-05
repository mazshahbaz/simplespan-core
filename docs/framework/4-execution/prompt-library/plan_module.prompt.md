---
title: Plan Template — Domain Module
version: 1.0
context: framework/4-execution/prompt-library
last_reviewed: 2025-10-05
ai_context: true
---

# Plan Template — Domain Module

Use this template to plan a **full module** (e.g., `section_properties`, `materials`, `loads`, `beam_effects`).

## Context (attach these paths)
- docs/framework/5-modules/module-planning-playbook.md
- docs/framework/5-modules/module-scaffolding-handoff-sop.md
- docs/framework/1-governance/coding-implementation-standards.md
- docs/framework/ai-response-protocol.md
- docs/framework/decisions/ADR-001-SI-units-and-metric.md
- docs/framework/decisions/ADR-004-domain-granularity.md

## Instruction
Produce the following Markdown files with YAML front-matter (`title, version, context, last_reviewed, ai_generated: true`), SI units, and inline CHBDC/CSA citations where applicable. Do **not** write code yet—this is planning only.

### Deliverables
1) **module-requirements.md**  
   - Intent, in-scope / out-of-scope  
   - Inputs/Outputs with units & valid ranges  
   - Assumptions & constraints (cite clauses)  
   - References (CHBDC/CSA, textbooks)

2) **module-design-brief.md**  
   - Layer placement & dependency rules  
   - Public API sketch (functions/classes, typed signatures)  
   - Algorithms outline w/ numerical notes  
   - Data structures (dataclasses/TypedDict)  
   - Risks & mitigations

3) **validation-plan.md**  
   - Cases table (ID, Summary, Inputs, Expected, Source, Tolerance)  
   - File locations for `tests/validation/<module>/cases/*.json`

4) **module-roadmap.md**  
   - Milestones M1–M5 with acceptance gates  
   - Links to ADRs and CI requirements

## I/O Contract (fill for the target module)
- Inputs: name, type, units, allowed range, defaults
- Outputs: name, type, units, precision policy

## Acceptance Checklist
- [ ] SI units only; inline CHBDC/CSA where applicable  
- [ ] Front-matter present; ai_generated: true  
- [ ] Interfaces documented with typed signatures  
- [ ] Validation plan includes tolerances and sources  
- [ ] Cross-links to ADRs and framework docs  
- [ ] Append an entry to `/ai-log/*.jsonl` and update `CHANGELOG.md`