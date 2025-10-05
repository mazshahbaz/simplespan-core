---
title: SimpleSpan AIC Sub-Project Architecture
version: 1.0
context: ai/automation/architecture
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# 🏗️ SimpleSpan AIC Enablement & Automation — System Architecture

This document illustrates how the **AIC Enablement & Automation Sub-Project** integrates into the broader SimpleSpan Core Framework.

## ASCII Architecture Diagram

```
                           ┌──────────────────────────────────────────────────┐
                           │            SimpleSpan Core Repository            │
                           │  (docs, src, tools, tests, .github, reports)     │
                           └──────────────────────────────────────────────────┘
     ┌──────────────────────────────────────────┬──────────────────────────────────────────┐
     │                                          │                                          │
     ▼                                          ▼                                          ▼
┌──────────────┐                         ┌────────────────┐                         ┌──────────────────────┐
│ Governance   │                         │ Documentation  │                         │ Source Code & Tests │
│ Layer        │                         │ Layer          │                         │ (src/, tests/)      │
│ - Playbook   │                         │ - v4.0 Plan    │                         │ - Domain modules    │
│ - Oaths/KPIs │                         │ - Roadmaps     │                         │ - FEA, etc.         │
│ - ADRs       │                         │ - ADRs/Specs   │                         │ - Validation seeds  │
└─────┬────────┘                         └────────┬───────┘                         └──────────┬──────────┘
      │                                          │                                          │
      ▼                                          ▼                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             AIC Enablement & Automation Sub-Project                                 │
│                                                                                                      │
│  ┌──────────────┐    ┌──────────────────────┐    ┌────────────────────────┐    ┌──────────────────┐  │
│  │ AIC_README   │    │ aic_orchestrator.py │    │ Guardrails/Router      │    │ Schema Validator │  │
│  │ (protocols)  │    │ (context + next     │    │ (route_task allowlist, │    │ (front-matter    │  │
│  │ roles, SOP)  │    │ tasks, acceptance)  │    │ diff caps, stop rules) │    │ & manifest)      │  │
│  └──────┬───────┘    └──────────┬──────────┘    └──────────────┬─────────┘    └──────────┬───────┘  │
│         │                       │                                │                         │          │
│         ▼                       ▼                                ▼                         ▼          │
│  ┌──────────────┐      ┌────────────────┐                 ┌──────────────┐           ┌────────────────┐│
│  │ Progress Log │◀────▶│ CI / GitHub    │◀───────────────▶│ CCP Helper   │           │ Audit & Reports ││
│  │ reports/*.md │      │ Workflows      │                 │ create_ccp.py│           │ docs_audit,    ││
│  └──────────────┘      │ (issue → run   │                 └──────────────┘           │ governance.html││
│                         │ orchestrator) │                                             └────────────────┘│
│                         └────────────────┘                                                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
      ▲                                          ▲                                          ▲
      │                                          │                                          │
      │                 ┌───────────────────────────────────────────────────────────┐       │
      │                 │         External AI Agents (under AIC supervision)       │       │
      │                 │  - Planner  - Implementer  - Reviewer  - Auditor         │       │
      │                 └───────────────────────────────────────────────────────────┘       │
      │                                          ▲                                          │
      └──────────────────────────────────────────┼──────────────────────────────────────────┘
                                                 │
                                        ┌────────┴────────┐
                                        │ Human Supervisor │
                                        │ (approve/merge,  │
                                        │  tag CCPs)       │
                                        └──────────────────┘
```

## Interpretation

- **AIC_README.md** – Defines the policies, guardrails, and protocols that all AI agents must obey.  
- **aic_orchestrator.py** – Reads project context (from v4.0 plan) and proposes next tasks safely.  
- **Guardrails/Router** – Restricts file access, enforces diff caps, and logs potential violations.  
- **Schema Validator** – Ensures all documentation and metadata conform to defined schemas.  
- **CI/GitHub** – Automates task reporting, validation, and orchestration feedback loops.  
- **CCP Helper** – Creates cryptographically verifiable continuity checkpoints.  
- **Progress Log** – Tracks incremental progress, AI actions, and human approvals.

---

*Prepared by SimpleSpan Core Governance — 2025-10-05*
