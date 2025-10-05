---
title: SimpleSpan AIC Execution Flow
version: 1.0
context: ai/automation/execution
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# 🔁 SimpleSpan AIC Sub-Project — Execution Flow

This diagram shows how one work cycle operates within the **AIC orchestration framework**.

## ASCII Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1) Start Session                                                            │
│    - Human or AI opens repo                                                 │
│    - Run `aic_orchestrator.py`                                              │
│    - Orchestrator reads:                                                    │
│        resume_context (from v4.0 plan)                                      │
│        progress.md (latest status)                                          │
│        current phase + checklist                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2) Propose Micro-Plan                                                       │
│    - Orchestrator outputs next 1–3 tasks                                   │
│    - Candidate paths (allowlist only), acceptance checks, risks            │
│    - Human supervisor reviews                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3) Execute Safely                                                           │
│    - (Option A) Human implements small changes                              │
│    - (Option B) AIC delegates to sub-agents (Planner→Implementer→Reviewer) │
│    - Router/guardrails enforce path caps & diff size                        │
│    - Schema validator + docs_audit run                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4) Log & Validate                                                           │
│    - Update checkboxes in phase checklist                                   │
│    - Append a line to reports/progress.md                                   │
│    - CI workflows verify audits/tests                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5) Phase Acceptance?                                                        │
│    - If checklist + acceptance pass → orchestrator proposes CCP tag & cmds  │
│    - Human approves and runs git tag + push                                 │
│    - Progress table updated (phase %; CCP column)                           │
└─────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 6) Advance                                                                  │
│    - resume_context.current_phase incremented                               │
│    - Next session starts from new phase automatically                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Summary
The AIC orchestrates micro-tasks between humans and agents in short, auditable loops.  
Each session maintains full traceability and safe progression through the refinement plan.

---

*Prepared by SimpleSpan Core Governance — 2025-10-05*
