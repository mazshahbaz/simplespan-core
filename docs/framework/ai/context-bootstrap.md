---
title: SimpleSpan AI Context Bootstrap Protocol
version: 1.0
context: ai/governance/context-bootstrap
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# 🧭 SimpleSpan Framework — AI Context Bootstrap Protocol

## 1. Preface
This document establishes the **official procedure** for rehydrating AI operational context within the SimpleSpan Framework.  
It ensures continuity of governance, reproducibility of context, and compliance with the SimpleSpan AI Governance System.

All agents and AI operators **must follow this protocol** prior to initiating or resuming any SimpleSpan-related operation.  
This procedure is recognized under governance authority of **SimpleSpan Core Framework (v4.0)** and its **AIC Enablement & Automation Sub-Project**.

---

## 2. Scope
This protocol applies to all AI entities (AIC, Planner, Implementer, Reviewer, Auditor) and all human supervisors initiating a session involving:
- Framework planning, design, or coding.
- Module or domain development.
- Governance or documentation operations.
- Auditing or CCP (Continuity Checkpoint) verification.

---

## 3. Canonical Procedure (Rehydration Sequence)

### Step 1 — Declare Context
Begin every session by declaring:

> "Load context from the SimpleSpan repository.  
> The active project is **SimpleSpan Core**, with the **AIC Enablement & Automation Sub-Project**.  
> Resume from Phase 1 — Governance & Policy Integration."

This declaration activates continuity tracking and identifies the current operational phase.

---

### Step 2 — Reference Core Governance Documents
Load the following documents (in order) to establish base state:

1. **Primary Framework Plan**  
   `docs/framework/1-governance/simple-span-framework-refinement-plan-v4.0.md`

2. **AIC Sub-Project Roadmap**  
   `docs/framework/ai/aic-subproject/roadmap.md`

3. **AIC Operational Readme**  
   `docs/framework/ai/aic-subproject/README.md`

4. **Orchestrator Configuration**  
   `tools/aic_orchestrator.config.yaml`

5. **Progress and Logging Data**  
   `reports/progress.md`

---

### Step 3 — Reference Optional Domain Documents
If the operation pertains to a specific module or domain, also reference:

- `docs/framework/ai/plan-schema.md`
- `examples/plans/section-properties-plan-sample.md`
- Any relevant domain roadmap under `docs/<domain>/`

---

### Step 4 — Verify Resume Context
Confirm that `resume_context` is present and valid within the active plan.  
It must include:

```yaml
resume_context:
  current_phase: <int>
  last_ccp: <string>
  progress_file: reports/progress.md
```

Verify:
- The phase number matches the intended operational phase.  
- The CCP tag aligns with the last recorded checkpoint.  
- The progress log exists and is readable.

---

### Step 5 — Confirm Readiness and Begin
Once verification is complete, the agent must declare readiness:

> "Context verified. SimpleSpan operational continuity confirmed.  
> Resuming AIC operations under Phase X in accordance with governance protocol."

Operations may then proceed under existing governance, validation, and guardrail rules.

---

## 4. Verification Checklist
| # | Verification Item | Status |
|---|-------------------|--------|
| 1 | Context declaration made | [ ] |
| 2 | Core documents loaded | [ ] |
| 3 | Resume context validated | [ ] |
| 4 | Progress file accessible | [ ] |
| 5 | Phase verified and declared | [ ] |

Agents must complete this checklist before beginning operations.

---

## 5. Compliance Notice
All AI and human operators must adhere to these policies:

- The **SimpleSpan AI Governance Policy** and **AIC Operational Handbook** are binding.  
- All actions are subject to validation, CCP creation, and progress logging.  
- No edits may exceed guardrail caps (12 files, 600 lines) unless explicitly approved.  
- Failure to follow this protocol invalidates AI-generated outputs pending manual audit.

---

## 6. Appendix — Example Initialization Prompts

### (a) AIC Initialization Prompt
> "Initialize AIC operations using the SimpleSpan Context Bootstrap Protocol.  
> Load active governance and orchestration context.  
> Verify Phase and CCP state from `simple-span-framework-refinement-plan-v4.0.md`.  
> Propose the next 1–3 actionable items under current phase checklist."

### (b) Planner Agent Prompt
> "Act as the Planner Agent within the SimpleSpan Framework.  
> Reference the AIC roadmap and plan-schema.  
> Propose micro-plans for the current phase, ensuring schema compliance and audit traceability."

### (c) Implementer Agent Prompt
> "Act as the Implementer Agent within the SimpleSpan Framework.  
> Implement tasks assigned by the AIC or Planner Agent.  
> Follow guardrails, SI/CHBDC compliance, and update progress.md upon completion."

### (d) Reviewer Agent Prompt
> "Act as the Reviewer Agent within the SimpleSpan Framework.  
> Review all outputs for schema validity, compliance, and adherence to governance tone.  
> Record findings in reports/ai/reviews/."

### (e) Auditor Agent Prompt
> "Act as the Auditor Agent within the SimpleSpan Framework.  
> Validate continuity, CCP creation, and schema compliance.  
> Report deviations in governance dashboard or `reports/ai/audit-log.yaml`."

---

## 7. Authority and Maintenance
This protocol is maintained under the authority of the **SimpleSpan Governance Board** and forms part of the official AI Operational Framework.  
Revisions must be recorded as ADRs within `docs/framework/1-governance/adrs/` and approved via CCP.

---

*Prepared by SimpleSpan Core Governance — 2025-10-05*
