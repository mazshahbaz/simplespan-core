---
title: Plan Template — Feature
version: 1.0
context: framework/4-execution/prompt-library
last_reviewed: 2025-10-05
ai_context: true
---

# Plan Template — Feature

Use this template to plan a **feature inside a module** (e.g., FEA moving-load envelopes, cracked-section visualization, polygon holes).

## Context (attach these paths)
- docs/framework/ai-response-protocol.md
- docs/framework/1-governance/coding-implementation-standards.md
- docs/framework/decisions/ADR-001-SI-units-and-metric.md
- docs/framework/decisions/ADR-004-domain-granularity.md
- (Add domain-specific specs, e.g. `docs/framework/6-fea/*` for FEA features)

## Instruction
Produce the following Markdown files with YAML front-matter (`title, version, context, last_reviewed, ai_generated: true`), SI units, and inline CHBDC/CSA citations where applicable. Do **not** write code yet—this is planning only.

### Deliverables
1) **feature-plan.md**  
   - Objective, scope, dependencies  
   - I/O tables with units and valid ranges  
   - Assumptions & standards citations

2) **feature-design.md**  
   - Interfaces (functions/classes) and typed signatures  
   - Algorithms/data flow (ASCII)  
   - Performance & precision notes

3) **validation-plan.md**  
   - Benchmarks, sources, tolerances  
   - Example JSON case schema

4) **feature-roadmap.md**  
   - M1–M5 milestones and acceptance gates

## I/O Contract (fill for the target feature)
- Inputs: …  
- Outputs: …

## Acceptance Checklist
- [ ] SI units only; inline CHBDC/CSA where applicable  
- [ ] Front-matter present; ai_generated: true  
- [ ] Interfaces documented with typed signatures  
- [ ] Validation plan includes tolerances and sources  
- [ ] Cross-links to ADRs and framework docs  
- [ ] Append an entry to `/ai-log/*.jsonl` and update `CHANGELOG.md`