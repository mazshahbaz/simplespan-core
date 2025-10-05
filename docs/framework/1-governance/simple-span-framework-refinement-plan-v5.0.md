---
title: SimpleSpan Framework Refinement Plan
version: 5.0
context: governance/framework
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
supersedes: docs/framework/1-governance/simple-span-framework-refinement-plan-v4.0.md
ccp_reference: vCORE-5.0-ccp-baseline
resume_context:
  current_phase: 0
  last_ccp: vCORE-4.0-ccp-final
  progress_file: reports/progress.md
---

# 🧭 SimpleSpan Framework Refinement Plan (v5.0)

This roadmap marks the **transition from human-managed to AI-integrated governance** for the SimpleSpan Framework.
It supersedes v4.0 and defines the procedures, standards, and performance metrics governing AI, human, and hybrid
operations under the SimpleSpan ecosystem.

---

## 📘 Executive Summary

Version 5.0 introduces **AI co-governance** and full schema-based automation of the development lifecycle. It unifies
policy, operations, validation, and audit under the SimpleSpan AI Governance Framework, leveraging:

- **AIC Orchestrator** for task generation and validation.
- **Schema-based control** via `plan-schema.md` and `logging-schema.md`.
- **Continuity** ensured through `context-bootstrap.md` and `progress.md`.
- **Automated traceability** using `aic_logger.py`, `schema_validator.py`, and CI enforcement.

The roadmap is divided into eight structured phases, forming a continuous improvement loop.

---

## 🧱 Phase Summary Table

| Phase | Title                           | Key KPIs                | CCP Reference               |
|------:|---------------------------------|-------------------------|-----------------------------|
| 0     | Continuity & Genesis            | Activation complete     | vCORE-5.0-ccp-baseline      |
| 1     | AI Governance Integration       | ≥98% schema compliance  | vCORE-5.0-ccp-governance    |
| 2     | Validation & Logging Automation | 100% logging coverage   | vCORE-5.0-ccp-validation    |
| 3     | Modular Intelligence Integration| Agents operational      | vCORE-5.0-ccp-integration   |
| 4     | Human-AI Collaboration Protocols| ≥90% review pass rate   | vCORE-5.0-ccp-collab        |
| 5     | Telemetry & Reporting Framework | ≥95% data uptime        | vCORE-5.0-ccp-telemetry     |
| 6     | Expansion & Domain Scaling      | 3 domains operational   | vCORE-5.0-ccp-domains       |
| 7     | CCP Audit & Lifecycle Mgmt      | 100% CCP verified       | vCORE-5.0-ccp-audit         |

---

## 🔁 Circular Lifecycle Diagram

```
          ┌────────────────────────────┐
          │   Phase 0: Continuity &    │
          │          Genesis           │
          └──────────────┬─────────────┘
                         │
                         ▼
      ┌────────────────────────────────────┐
      │ Phase 1: AI Governance Integration │
      └────────────────────┬───────────────┘
                           ▼
        ┌─────────────────────────────────┐
        │ Phase 2: Validation & Logging   │
        └────────────────────┬────────────┘
                             ▼
          ┌────────────────────────────────────┐
          │ Phase 3: Modular Intelligence      │
          └────────────────────┬───────────────┘
                               ▼
            ┌─────────────────────────────────────┐
            │ Phase 4: Human–AI Collaboration     │
            └────────────────────┬────────────────┘
                                 ▼
              ┌─────────────────────────────────┐
              │ Phase 5: Telemetry & Reporting  │
              └────────────────────┬────────────┘
                                   ▼
                ┌─────────────────────────────────┐
                │ Phase 6: Domain Scaling         │
                └────────────────────┬────────────┘
                                     ▼
                  ┌──────────────────────────────────┐
                  │ Phase 7: CCP Audit & Lifecycle   │
                  └────────────────────┬──────────────┘
                                       │
                                       ▼
                         ◄─── Feedback Loop ────►
                         (Improvement → Genesis)
```

---

# 🧩 Phases

## Phase 0 — Continuity & Genesis
### 🎯 Objective
Transition from v4.0 to AI-native governance. Establish continuity checkpoints and activate v5.0.

### ⚙️ Dependencies
None (initial baseline).

### ✅ Checklist
- [x] Freeze v4.0 roadmap and record CCP tag (`vCORE-4.0-ccp-final`).
- [x] Add supersedes notice in v5.0 front-matter.
- [ ] Activate AIC orchestrator configuration (`tools/aic_orchestrator.config.yaml`).
- [ ] Initialize `reports/progress.md` and `reports/ai/sessions/` (progress log active; sessions/ pending).
- [ ] Log a baseline AIC session using `tools/ai/aic_logger.py`.

### 📄 Deliverables
- CCP `vCORE-5.0-ccp-baseline` (recorded in `reports/ai/ccp/`).
- Updated governance index linking v4.0 → v5.0.
- Baseline entry in `reports/progress.md`.

### 📈 Metrics (KPIs)
| KPI                      | Target | Verification                 |
|--------------------------|--------|------------------------------|
| Baseline recorded        | Yes    | `reports/progress.md` entry  |
| Orchestrator configured  | Yes    | Config audit in CI           |

### ⚠️ Risks & Mitigations
- **Continuity loss** → Run manual audit of v4.0 → v5.0 link; keep dual copies of CCP.

### 🧭 Escalation Protocol
Human → Auditor → Governance Board.

### 🔗 References
`docs/framework/ai/context-bootstrap.md`, `reports/progress.md`.

---

## Phase 1 — AI Governance Integration
### 🎯 Objective
Embed AI co-governance layer across all operations and validate plan compliance.

### ⚙️ Dependencies
Phase 0.

### ✅ Checklist
- [ ] Implement `aic_orchestrator.config.yaml` defaults (plan path, progress path, caps).
- [ ] Verify all plans conform to `plan-schema.md` (front-matter + checklist format).
- [ ] Run AIC orchestration dry-run and capture output in `reports/ai/sessions/`.
- [ ] Add “Context Bootstrap Protocol” to onboarding docs.

### 📄 Deliverables
- Updated orchestrator config and bootstrap policy.
- Validated plan documents (schema-compliant).

### 📈 Metrics (KPIs)
| KPI                 | Target | Tool/Verification          |
|---------------------|--------|----------------------------|
| Schema compliance   | ≥98%   | `schema_validator.py` (CI) |
| Bootstrap readiness | 100%   | Manual spot check          |

### ⚠️ Risks & Mitigations
- **Misconfigured orchestrator** → Sandbox test (`--dry-run`) before enabling CI.

### 🧭 Escalation Protocol
AI → Reviewer → Governance Board.

### 🔗 References
`tools/aic_orchestrator.py`, `docs/framework/ai/plan-schema.md`, `docs/framework/ai/context-bootstrap.md`.

---

## Phase 2 — Validation & Logging Automation
### 🎯 Objective
Establish automatic validation and structured logging for all sessions.

### ⚙️ Dependencies
Phase 1.

### ✅ Checklist
- [ ] Deploy `tools/ai/aic_logger.py` to write session YAMLs.
- [ ] Enforce `logging-schema.md` through CI on pushes and PRs.
- [ ] Create sample session logs and a failing example for CI negative tests.
- [ ] Add a progress gating rule (require new dated line for progress edits).

### 📄 Deliverables
- Active logging system + CI validation.
- Example logs in `examples/logs/`.

### 📈 Metrics (KPIs)
| KPI                  | Target | Verification     |
|----------------------|--------|------------------|
| Log schema compliance| 100%   | CI check         |
| Log coverage         | 100%   | Progress audit   |

### ⚠️ Risks & Mitigations
- **Incomplete logs** → CI job fails if session logs missing for relevant commits.

### 🧭 Escalation Protocol
Reviewer → Auditor → Governance Board.

### 🔗 References
`tools/ai/aic_logger.py`, `docs/framework/ai/logging-schema.md`, `.github/workflows/*.yml`.

---

## Phase 3 — Modular Intelligence Integration
### 🎯 Objective
Define and deploy Planner, Implementer, Reviewer agents with clear interfaces and handoffs.

### ⚙️ Dependencies
Phase 2.

### ✅ Checklist
- [ ] Define role responsibilities and limits (guardrails: 12 files / 600 lines).
- [ ] Configure planner-agent prompt templates and examples.
- [ ] Document inter-agent workflow (ASCII diagram) and escalation triggers.
- [ ] Add examples of acceptable outputs (plans, diffs, review notes).

### 📄 Deliverables
- Agent role definitions, prompt templates, and workflow diagrams.

### 📈 Metrics (KPIs)
| KPI                 | Target | Verification        |
|---------------------|--------|---------------------|
| Role clarity        | 100%   | Governance review   |
| Workflow reliability| ≥95%   | AIC trial runs      |

### ⚠️ Risks & Mitigations
- **Role confusion** → Governance index updated; examples included.

### 🧭 Escalation Protocol
Planner → Reviewer → Governance Board.

### 🔗 References
`docs/framework/ai/aic-subproject/roadmap.md`, `docs/framework/ai/aic-subproject/README.md`.

---

## Phase 4 — Human–AI Collaboration Protocols
### 🎯 Objective
Establish procedures for joint decision-making, escalation, and approvals.

### ⚙️ Dependencies
Phase 3.

### ✅ Checklist
- [ ] Define review turnaround times and priority classes (P0–P2).
- [ ] Create reviewer & auditor guidelines (acceptance criteria, schema checks).
- [ ] Add escalation chart and expected SLAs (48–72h).

### 📄 Deliverables
- Collaboration policy doc, updated governance playbook.

### 📈 Metrics (KPIs)
| KPI                     | Target | Verification |
|-------------------------|--------|--------------|
| Review acceptance rate  | ≥90%   | Audit        |
| Issue resolution latency| <72h   | Progress log |

### ⚠️ Risks & Mitigations
- **Review fatigue** → Phased scheduling and batching.

### 🧭 Escalation Protocol
AI → Reviewer → Auditor → Governance Board.

### 🔗 References
`docs/framework/1-governance/governance-playbook.md`.

---

## Phase 5 — Telemetry & Reporting Framework
### 🎯 Objective
Implement analytics and dashboards for governance insight and improvement.

### ⚙️ Dependencies
Phase 4.

### ✅ Checklist
- [ ] Activate metrics aggregation (`reports/ai/metrics/summary.json`).
- [ ] Update `reports/governance-dashboard.html` with live values.
- [ ] Schedule monthly report exports (CCP summary, acceptance metrics).

### 📄 Deliverables
- Active dashboard and monthly metrics report.

### 📈 Metrics (KPIs)
| KPI               | Target | Verification |
|-------------------|--------|--------------|
| Dashboard uptime  | ≥95%   | CI check     |
| Metrics refresh   | Weekly | Manual audit |

### ⚠️ Risks & Mitigations
- **Data loss** → Backups and periodic snapshots.

### 🧭 Escalation Protocol
Auditor → Governance Board.

### 🔗 References
`reports/governance-dashboard.html`, `reports/ai/metrics/`.

---

## Phase 6 — Expansion & Domain Scaling
### 🎯 Objective
Extend governance model to technical domains (e.g., Sections, FEA, Frames).

### ⚙️ Dependencies
Phase 5.

### ✅ Checklist
- [ ] Apply schema to Section Properties and FEA modules.
- [ ] Validate domain documentation & seed cases.
- [ ] Integrate modules with orchestrator and add prompts.

### 📄 Deliverables
- Domain plans validated; `section-properties-plan-sample.md` updated; seed cases added.

### 📈 Metrics (KPIs)
| KPI               | Target | Verification |
|-------------------|--------|--------------|
| Domains onboarded | ≥3     | Progress log |

### ⚠️ Risks & Mitigations
- **Overlap between modules** → Maintain domain registry and interfaces.

### 🧭 Escalation Protocol
Domain lead → Reviewer → Governance Board.

### 🔗 References
`examples/plans/section-properties-plan-sample.md`, `docs/framework/ai/plan-schema.md`.

---

## Phase 7 — CCP Audit & Lifecycle Management
### 🎯 Objective
Establish permanent CCP audit, verification, and retention cycle.

### ⚙️ Dependencies
Phase 6.

### ✅ Checklist
- [ ] Verify CCP tags for all phases and sub-projects.
- [ ] Archive old CCPs (>7 years) in PDF + YAML.
- [ ] Finalize retention policy and publish audit report.

### 📄 Deliverables
- CCP audit report; lifecycle retention document.

### 📈 Metrics (KPIs)
| KPI                    | Target | Verification  |
|------------------------|--------|---------------|
| CCP retention compliance| 100%  | Audit         |
| CCP verification        | 100%  | Governance GB |

### ⚠️ Risks & Mitigations
- **Incomplete records** → Dual verification before closing audits.

### 🧭 Escalation Protocol
Auditor → Governance Board → Legal Advisor.

### 🔗 References
`reports/ai/ccp/`, `docs/framework/1-governance/adrs/`.

---

# 📚 Appendices

## Appendix A — Metrics Schema
| Metric            | Definition                               | Target | Phase |
|-------------------|-------------------------------------------|--------|-------|
| Schema compliance | % documents passing plan-schema           | ≥98%   | 1     |
| Logging coverage  | Sessions logged / total sessions          | 100%   | 2     |
| Review acceptance | % reviewed outputs approved               | ≥90%   | 4     |
| Dashboard uptime  | % of time dashboard served                | ≥95%   | 5     |
| Domain adoption   | # of modules onboarded                    | ≥3     | 6     |
| CCP audit pass    | % CCPs verified                           | 100%   | 7     |

## Appendix B — Escalation Chain
AI → Reviewer → Auditor → Governance Board → Legal Advisor
- Expected max turnaround per tier: 48 hours.

## Appendix C — Retention Policy
| Artifact | Retention | Format   |
|----------|-----------|----------|
| CCPs     | ≥7 years  | YAML+PDF |
| Logs     | 12 months | YAML     |
| Metrics  | Permanent | JSON     |
| Reports  | Permanent | HTML/PDF |

## Appendix D — Cross-Reference Index
| Document                | Path                                                     | Type       |
|-------------------------|----------------------------------------------------------|------------|
| Plan Schema             | docs/framework/ai/plan-schema.md                         | Schema     |
| Logging Schema          | docs/framework/ai/logging-schema.md                      | Schema     |
| Context Bootstrap       | docs/framework/ai/context-bootstrap.md                   | Procedure  |
| Governance Playbook     | docs/framework/1-governance/governance-playbook.md       | Policy     |
| AIC Roadmap             | docs/framework/ai/aic-subproject/roadmap.md              | Roadmap    |
| Section Properties Plan | examples/plans/section-properties-plan-sample.md         | Example    |
| Progress Log            | reports/progress.md                                      | Operational|

---

*Prepared under authority of the SimpleSpan Governance Board — 2025-10-05*
