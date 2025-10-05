---
title: SimpleSpan: The Agentic Framework for AI-Native Structural Engineering
version: 1.0
last_reviewed: 2025-10-05
---

# SimpleSpan: The Agentic Framework for AI-Native Structural Engineering

## Executive Summary
SimpleSpan introduces a governed framework for developing structural engineering software with artificial intelligence.
It combines engineering standards, schema-based governance, and multi-agent orchestration to automate and document the full software lifecycle.
Each AI role—Planner, Implementer, Reviewer, and Auditor—operates under an AI Coordinator (AIC) that manages intent, ensures compliance, and records results.
The framework enables autonomous module generation while maintaining full traceability and CHBDC/SI code alignment.
It provides engineers a reliable way to scale analysis and design software while preserving professional accountability.

## 1. Introduction
Structural engineering software remains fragmented and manually developed.
Existing tools are domain-bound and slow to adapt to new codes or methods.
The SimpleSpan framework addresses this by creating a unified, schema-governed system that integrates AI agents into the development process.
Each agent follows engineering rules, producing consistent and verifiable results.
AIC acts as a coordinator—translating human intent into structured tasks, assigning agents, validating outputs, and maintaining audit records.

## 2. Vision and Philosophy
SimpleSpan applies *agentic engineering*: structured collaboration between humans and AI under governance.
Agents think and act independently but are bound by standards, schemas, and validation.
Human engineers define objectives and rules; AI executes within those limits.
Each generation of the framework refines itself through Continuity Checkpoints (CCPs) and metrics, ensuring reliability, transparency, and interoperability.

## 3. Framework Architecture
```
Governance Layer   → Schemas, standards, CCPs, ADRs
AIC Orchestration  → Intent parsing, role routing, validation
Agent Layer        → Planner · Implementer · Reviewer · Auditor
Domain Layer       → Structural modules (Sections, FEA, Materials)
Execution Layer    → Tools, CI/CD, dashboards, reports
```
The governance layer defines laws and schemas; AIC manages workflows; agents execute; domains hold technical logic; execution validates and reports.

## 4. AI Coordinator (AIC)
The AIC is the control core.
It parses intent, routes tasks, validates output, records sessions, and manages CCPs.
It enforces schema compliance and structured behavior.

Core functions:
- Parse intents
- Route to agents
- Validate outputs
- Record sessions and CCPs
- Update manifests

## 5. Agentic Coding Model
| Role | Function | Artifact |
|------|-----------|----------|
| Planner | Create structured plan | Plan |
| Implementer | Build code per plan | Source + Tests |
| Reviewer | Validate and check | Logs |
| Auditor | Verify metrics and CCPs | Reports |

Each role uses hybrid YAML/Markdown prompts and a closed loop of intent → plan → code → review → audit → refinement.

## 6. Technology Stack
| Layer | Technology |
|--------|-------------|
| Core | Python 3 |
| Schemas | YAML + Markdown |
| Automation | GitHub Actions |
| AI | Claude, GPT, Cursor |
| Validation | schema_validator.py, manifest_generator.py |
The system is open, explainable, and reproducible.

## 7. Domains
**Sections**: standard/composite sections, cracked analysis, visualization.  
**FEA**: frame and multi-span analysis, moving loads, envelopes.  
Future: materials, bridges, dynamics, design automation.

## 8. Governance Lifecycle
```
Intent → Plan → Implementation → Review → Audit → CCP → Feedback
```
Each step is schema-validated and logged for traceability and improvement.

## 9. Roadmap
| Phase | Focus | Output |
|-------|--------|--------|
| 0 | Governance | Schemas, CCP |
| 1 | Sections | Domain module |
| 2 | FEA | Analysis code |
| 3 | AIC Orchestration | Full role routing |
| 4 | Dashboard | Metrics visualization |
| 5 | AI-Driven Improvement | Self-tuning agents |
| 6+ | Expansion | New domains |

## 10. Impact
- **Engineers:** Reduces manual coding, enforces standards.  
- **Industry:** Creates interoperable, traceable tools.  
- **Research:** Demonstrates governed AI for engineering.

## 11. Future Vision
Autonomous but governed evolution:
parallel agents, live code updates, self-validation, and collaborative AI-human design.

## 12. Conclusion
SimpleSpan merges AI capability with engineering discipline.
It builds reliable, auditable, and continuously improving systems for structural design.
