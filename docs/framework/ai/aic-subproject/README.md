---
title: AIC Enablement & Automation — Sub-Project README
version: 1.0
context: ai/automation/readme
schema_version: 1
last_reviewed: 2025-10-05
ai_context: true
---

# 🧭 SimpleSpan — AIC Enablement & Automation (Sub-Project)

This sub-project provides the **AI governance & automation layer** for SimpleSpan.
It defines *how* AI (and humans) operate safely: planning, guardrails, validation, logging, and CCPs.

**Core artifacts**
- `AIC_README.md` — Playbook for agents & humans (protocols, guardrails, SOPs)
- `tools/aic_orchestrator.py` — Read-only CLI that reads a plan and proposes next micro-tasks
- `tools/aic_orchestrator.config.yaml` — Defaults (plan path, allowlist, diff caps)
- `docs/framework/ai/aic-subproject/roadmap.md` — 7-phase build-out plan for this layer
- Diagrams: `architecture.md`, `execution-flow.md`
- Logs & reports in `reports/`

---

## ✅ Quick Start (2 minutes)

1. **Install files** (ensure they’re in the repo):
   - `docs/framework/ai/AIC_README.md`
   - `tools/aic_orchestrator.py`
   - `tools/aic_orchestrator.config.yaml`

2. **Run the orchestrator** from repo root:
   ```bash
   python tools/aic_orchestrator.py
   # JSON for agents/CI:
   python tools/aic_orchestrator.py --json
   # Override a specific plan:
   python tools/aic_orchestrator.py --plan path/to/another-plan.md
   ```

3. **Act on 1–3 micro-tasks** it suggests. Keep changes small, commit locally.

4. **Log your step** by appending one line to `reports/progress.md`.

5. **When a phase checklist completes**:
   - Orchestrator will propose a **CCP tag** and `git` commands.
   - You (human) run them and push.

> Guardrails (enforced by policy and router): SI units, CHBDC citations by clause ID, allowlisted paths only, ≤ 12 files and ≤ 600 lines per run, stop if CI/audit fails twice.

---

## 🌳 Framework-Aware, Project-Agnostic

**The AIC is *not* chained to any specific plan (e.g., v4.0).** It’s **rooted** in the SimpleSpan schema and can read **any** plan that follows our format:

- `resume_context` fenced YAML block with `current_phase`, `last_ccp`, `progress_file`
- Phases formatted as `## Phase N — Title`
- Per-phase `### ✅ Checklist` with `- [ ]` items

**Switch plans at any time**:
```bash
python tools/aic_orchestrator.py --plan docs/fea/fea-plan-v1.0.md
```

**Conceptual model**:
```
AIC (agents + orchestrator)
          │  reads
          ▼
Any plan file following SimpleSpan schema
(v4.0 today; FEA plan tomorrow; external repo later)
```

---

## 🧩 Configuration (`tools/aic_orchestrator.config.yaml`)

```yaml
default_plan: docs/framework/1-governance/simple-span-framework-refinement-plan-v4.0.md
default_progress: reports/progress.md

allowlist:
  - docs/**
  - tools/**
  - src/simplespan_*/**
  - tests/**
  - .github/**
  - .ai/**
  - reports/**
  - validation/**

caps:
  files: 12
  lines: 600
```

**Rules**
- CLI flags override config values.
- If config missing, orchestrator falls back to internal defaults.

---

## 🧾 Plan Schema (Mini-Spec)

A plan file must include:

- **Front-matter**:
  ```yaml
  ---
  title: <name>
  version: <semver or int>
  context: <area>
  schema_version: 1
  last_reviewed: <YYYY-MM-DD>
  ai_context: true
  ---
  ```

- **YAML Resume Context** fenced block:
  ```yaml
  resume_context:
    current_phase: <int>
    last_ccp: <string>
    progress_file: <path>
  ```

- **Phase sections & checklists**:
  ```markdown
  ## Phase N — Title
  ### ✅ Checklist
  - [ ] Task 1
  - [x] Task 2
  ```

For a full specification, see `docs/framework/ai/plan-schema.md` (recommended next file).

---

## 🔁 Post-Phase Operations (Permanent Value)

After the AIC sub-project phases are complete, this layer becomes your **ongoing AI operations standard**:

- **Governance** — AIC enforces policy, schema, and guardrails continuously.
- **Planning** — Orchestrator suggests micro-tasks from any active plan.
- **Validation** — CI runs schema + docs audit every PR.
- **Continuity** — CCP helper tags milestones with manifest hashes.
- **Learning** — Telemetry dashboard tracks agent performance and errors over time.

---

## 🔗 Related Documents

- Roadmap: `docs/framework/ai/aic-subproject/roadmap.md`
- Architecture: `docs/framework/ai/aic-subproject/architecture.md`
- Execution flow: `docs/framework/ai/aic-subproject/execution-flow.md`
- Core plan: `docs/framework/1-governance/simple-span-framework-refinement-plan-v4.0.md`
- Playbook: `docs/framework/1-governance/governance-playbook.md`

---

## 🧪 Next Recommended Artifacts

- `docs/framework/ai/plan-schema.md` — full spec + examples
- `examples/plans/fea-plan-sample.md` — portable demo plan
- `tools/tests/test_plan_portability.py` — smoke test across multiple plans

---

*Prepared by SimpleSpan Core Governance — 2025-10-05*
