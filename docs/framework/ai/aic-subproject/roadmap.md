---
title: SimpleSpan AIC Enablement & Automation Roadmap
version: 1.0
context: ai/automation
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# 🧭 SimpleSpan Sub-Project — AIC Enablement & Automation Roadmap (v1.0)

## 📘 Overview
This sub-project defines the structured plan for building, standardizing, and governing all components that enable AI-assisted operations inside the **SimpleSpan Core Framework**.  
It ensures that every automation, agent, and CI process operates under auditable governance, reproducibility, and safety.

**Parent documents:**
- [simple-span-framework-refinement-plan-v4.0.md](../../1-governance/simple-span-framework-refinement-plan-v4.0.md)
- [governance-index.md](../../1-governance/governance-index.md)
- [AIC_README.md](../AIC_README.md)

---

## 📊 Progress Tracker

| Phase | Name | % Done | Status | CCP Tag | Notes |
|-------|------|--------|---------|----------|-------|
| 0 | Foundation & Context | ✅ 100% | Complete | vAIC-0-ccp-baseline | README + Orchestrator live |
| 1 | Governance & Policy Integration | 🟡 20% | In progress | — | Issue template draft |
| 2 | Schema & Validation Layer | ⚪ 0% | Pending | — | Planned |
| 3 | Guardrails & Safety Enforcement | ⚪ 0% | Pending | — | |
| 4 | Automation & CI Integration | ⚪ 0% | Pending | — | |
| 5 | CCP Automation & Validation | ⚪ 0% | Pending | — | |
| 6 | Onboarding & Documentation | ⚪ 0% | Pending | — | |
| 7 | Telemetry & Dashboards | ⚪ 0% | Pending | — | |

---

# ⚙️ Phases

## Phase 0 — Foundation & Context ✅
**Goal:** Establish core AIC infrastructure.  
**Deliverables:**  
- docs/framework/ai/AIC_README.md  
- tools/aic_orchestrator.py  
- reports/progress.md scaffold  
- CCP vAIC-0-ccp-baseline  
**Status:** Complete

---

## Phase 1 — Governance & Policy Integration
**Goal:** Embed AIC policies into governance and GitHub workflows.

### Actions
- [ ] Add .github/ISSUE_TEMPLATE/aic-run.yml
- [ ] Define labels ai:plan, ai:implement, ai:audit
- [ ] Add “AIC Operations Policy” to Governance Playbook
- [ ] Update system-inventory.md with AIC assets
- [ ] Run docs_audit.py --strict

### Deliverables
- Issue template + labels  
- Updated Playbook  
- ADR-040 “AIC Governance Integration”

### Acceptance Criteria
✅ Docs cross-linked ✅ CI green ✅ CCP vAIC-1-ccp-policy

---

## Phase 2 — Schema & Validation Layer
**Goal:** Standardize metadata & schema integrity.

### Actions
- [ ] Build tools/ai/schema_validator.py
- [ ] Add schema_manifest.json
- [ ] Integrate with docs_audit.py
- [ ] Fail CI on invalid schema

### Deliverables
- schema_validator.py, schema_manifest.json  
- ADR-041 “Schema Enforcement”  
**CCP:** vAIC-2-ccp-schema

---

## Phase 3 — Guardrails & Safety Enforcement
**Goal:** Enforce file/path restrictions & diff caps.

### Actions
- [ ] Add aic_orchestrator.config.yaml
- [ ] Update route_task.py to enforce caps
- [ ] Add pre-run guardrail check
- [ ] Log blocked actions → reports/ai/guardrail_log.json

### Deliverables
- Updated router + config  
- ADR-042 “Guardrails Enforcement”  
**CCP:** vAIC-3-ccp-guardrails

---

## Phase 4 — Automation & CI Integration
**Goal:** Automate planning & progress reporting via GitHub.

### Actions
- [ ] Create .github/workflows/aic-next-tasks.yml
- [ ] Post orchestrator output on issues labeled ai:plan
- [ ] Add CI tests for orchestrator
- [ ] Add reports/progress_bot.md

### Deliverables
- Workflow YAML  
- ADR-043 “AIC Automation Integration”  
**CCP:** vAIC-4-ccp-automation

---

## Phase 5 — CCP Automation & Validation
**Goal:** Simplify creation & verification of Continuity Checkpoints.

### Actions
- [ ] Build tools/create_ccp.py
- [ ] Generate ccp-manifest.json
- [ ] Add --propose-ccp to orchestrator
- [ ] Create CCP ADR template

### Deliverables
- CCP helper + manifest generator  
- ADR-044 “Automated CCPs”  
**CCP:** vAIC-5-ccp-helper

---

## Phase 6 — Onboarding & Documentation
**Goal:** Train humans & agents.

### Actions
- [ ] Write docs/onboarding/ai-handbook.md
- [ ] Add AIC + Orchestrator diagrams
- [ ] Add snippets/ (prompts, commands)
- [ ] Update Playbook onboarding section

### Deliverables
- AI Handbook + visuals  
- ADR-045 “AI Onboarding”  
**CCP:** vAIC-6-ccp-onboarding

---

## Phase 7 — Telemetry & Dashboards
**Goal:** Add visibility and long-term analytics.

### Actions
- [ ] Create reports/governance-dashboard.html
- [ ] Add metrics for audits, CCPs, AIC sessions
- [ ] Integrate with ai_summary.py
- [ ] Generate trend graphs

### Deliverables
- Governance Dashboard  
- ADR-046 “Governance Analytics & Telemetry”  
**CCP:** vAIC-7-ccp-dashboard

---

## 📈 KPIs & Governance Metrics

| Metric | Target | Verified By |
|---------|---------|-------------|
| Phase completion | 100 % per phase | reports/progress.md |
| Schema compliance | 100 % | schema_validator.py |
| Guardrail enforcement | 100 % | router logs |
| CCP creation time | ≤ 3 min | create_ccp.py |
| AIC task success rate | ≥ 95 % | progress.md entries |
| Context recovery | ≤ 15 min | context_rehydrate.py |

---

## 🔐 CCP Index

| CCP | Description |
|------|--------------|
| vAIC-0-ccp-baseline | AIC README + Orchestrator ready |
| vAIC-1-ccp-policy | Governance integration complete |
| vAIC-2-ccp-schema | Schema validator operational |
| vAIC-3-ccp-guardrails | Router guardrails enforced |
| vAIC-4-ccp-automation | CI automation active |
| vAIC-5-ccp-helper | CCP helper tools live |
| vAIC-6-ccp-onboarding | Human training complete |
| vAIC-7-ccp-dashboard | Telemetry dashboard online |

---

## 🪜 Governance Integration
This roadmap is cross-linked in the  
[governance-index.md](../../1-governance/governance-index.md) under  
**“AI / Automation Sub-Projects.”**

---

*Prepared by SimpleSpan Core Governance — 2025-10-05*
