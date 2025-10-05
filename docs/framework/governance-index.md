---
title: Governance Index — SimpleSpan Framework
version: 1.0
context: framework/governance-index
last_reviewed: 2025-10-05
ai_context: true
---

# 🧭 Governance Index — SimpleSpan Framework

> *“A single source of truth for structure, process, and collaboration — bridging human engineering discipline and AI-assisted development.”*

---

## 1. Overview

**SimpleSpan** is a modular structural-engineering suite designed for CHBDC/CSA-compliant analysis and design automation.  
This document serves as the **central map** of all governance, AI, and validation layers.

```
+-----------------------------+
|   1. Governance & Standards |
+-----------------------------+
             ↓
+-----------------------------+
|   2. Validation & QA Layer  |
+-----------------------------+
             ↓
+-----------------------------+
|   3. Shared Libraries       |
+-----------------------------+
             ↓
+-----------------------------+
|   4. Execution & AI Prompts |
+-----------------------------+
             ↓
+-----------------------------+
|   5. Domain Modules         |
+-----------------------------+
             ↓
+-----------------------------+
|   6. FEA & Analysis Engine  |
+-----------------------------+
```

---

## 2. Governance Hierarchy

| Category | Document | Purpose |
|-----------|-----------|----------|
| **Core Policy** | [`software-development-handbook.md`](1-governance/software-development-handbook.md) | Defines code and documentation expectations |
| **Coding Standards** | [`coding-implementation-standards.md`](1-governance/coding-implementation-standards.md) | Language, style, naming, testing, modular rules |
| **Change Policy** | [`change-management-policy.md`](../change-management-policy.md) | Commit, versioning, and changelog control |
| **Contributor Workflow** | [`contributor-playbook.md`](../contributor-playbook.md) | Human and AI contribution process |
| **AI Governance** | [`ai-response-protocol.md`](../ai-response-protocol.md) | Defines AI collaboration rules and quality gates |
| **Architecture Registry** | [`architecture-ascii-gallery.md`](../architecture-ascii-gallery.md) | ASCII diagrams of system structure |
| **Decision Records** | [`decisions/`](../decisions/) | Immutable ADRs (001–006) for key system decisions |
| **Governance Index (this doc)** | `governance-index.md` | Table of contents for all policies and processes |

---

## 3. Framework Layers

| Layer | Description | Primary Artifacts |
|--------|--------------|-------------------|
| **1. Governance** | Standards, ADRs, policies, and collaboration protocols | `/docs/framework/1-governance/` |
| **2. Validation** | Testing philosophy, verification methods, benchmarks | `/docs/framework/2-validation/` |
| **3. Libraries** | Shared schemas, materials, section definitions | `/docs/framework/3-libraries/` |
| **4. Execution** | Prompt templates, AI tooling, CI pipelines | `/docs/framework/4-execution/` |
| **5. Modules** | Domain-specific logic (sections, loads, materials) | `/docs/framework/5-modules/` |
| **6. FEA Engine** | Core analysis algorithms, solvers, envelopes | `/docs/framework/6-fea/` |

```
[Governance]
    ↓
[Validation]
    ↓
[Libraries] → [Execution (AI)]
    ↓
[Modules] → [FEA Engine]
```

---

## 4. AI Governance Ecosystem

| Component | File/Directory | Function |
|------------|----------------|-----------|
| **AI Router** | [`tools/ai/route_task.py`](../../tools/ai/route_task.py) | Classifies requests → emits prompts, context, and acceptance checklists |
| **Router Map (Planned)** | `tools/ai/router-map.yaml` | Declarative route configuration (Phase 4.1) |
| **AI Workspace Rules** | [`ai/workspace-rules.md`](ai/workspace-rules.md) | Always-on AI behavioral policy |
| **AI Response Protocol** | [`ai-response-protocol.md`](../ai-response-protocol.md) | Required context, metadata, and logging format |
| **AI Log** | [`/ai-log/`](../../ai-log/) | JSONL audit trail for every AI-generated output |
| **AI Log Schema** | [`ai_log_schema.json`](../../tools/ai/ai_log_schema.json) | Validates AI log format |
| **CI Workflow** | [`.github/workflows/docs-ci.yml`](../../.github/workflows/docs-ci.yml) | Automated validation, spellcheck, and AI compliance |
| **Audit Tools** | [`tools/docs_audit.py`](../../tools/docs_audit.py) | Merged linter, schema check, and freshness scanner (Phase 4.1) |

---

## 5. Human + AI Contribution Flow

```
[Plan]
  ↓
[Execute]
  ↓
[Review + Audit]
  ↓
[Merge + Tag]
  ↓
[Monitor + Summarize]
```

| Phase | Responsible | Tools / Prompts |
|--------|-------------|----------------|
| **Plan** | AI + Engineer | `plan_module.prompt.md` or `plan_feature.prompt.md` |
| **Execute** | AI | `module_scaffold.prompt.md`, `fea_module_scaffold.prompt.md` |
| **Review** | Human + CI | docs-ci.yml, docs_audit.py |
| **Merge** | Maintainer | Version bump + CHANGELOG update |
| **Summarize** | CI + AI | `ai_summary.py` → `ai-summary-YYYY-MM.md` |

---

## 6. CI & Automation Overview

| Stage | Tool | Description |
|--------|------|-------------|
| **Docs Context Index** | `tools/docs_audit.py` | Generates searchable index for AI context |
| **Front-Matter Validation** | `tools/docs_audit.py` | Ensures all docs have required metadata |
| **Link & Spell Check** | `markdown-link-check`, `cspell` | Keeps docs clean and consistent |
| **Schema Linting** | `jsonschema`, `pyyaml` | Validates YAML/JSON docs and logs |
| **AI Compliance** | Custom Python check | Verifies every `ai_generated: true` doc has ai-log entry |
| **Build Artifacts** | GitHub Actions | Uploads `context_index.json`, summaries |

---

## 7. Cross-Reference Matrix

| Topic | Document(s) | Tool(s) | Review Interval |
|--------|--------------|---------|----------------|
| **Governance Standards** | `software-development-handbook.md` | N/A | 180 days |
| **Coding Style & Tests** | `coding-implementation-standards.md` | CI | 180 days |
| **AI Collaboration** | `ai-response-protocol.md`, `workspace-rules.md` | `route_task.py`, `docs_audit.py` | 90 days |
| **Versioning** | `change-management-policy.md`, ADR-003 | `docs_audit.py` | 90 days |
| **FEA Philosophy** | ADR-006, `fea-architecture-and-design.md` | FEA solver modules | 120 days |
| **Validation Strategy** | `validation-verification-manual.md` | `docs_audit.py` | 180 days |

---

## 8. Change and Version Policy

- **Versioning:** Semantic Versioning (ADR-003)  
- **Changelog:** Every merge that alters outputs or structure must update `CHANGELOG.md`.  
- **AI Output:** Any `ai_generated: true` file must append an entry to `/ai-log/YYYY-MM-DD.jsonl`.  
- **Review:** All governance and AI files reviewed at least every **90 days** or upon tool update.  
- **Deprecation:** Old scripts (`docs_schema_lint.py`, `docs_context_index.py`) replaced by `docs_audit.py`.

---

## 9. Maintenance & Review Schedule

| Layer | Responsible | Interval |
|--------|-------------|-----------|
| Governance Docs | Lead Engineer | 90 days |
| ADRs | CTO / Reviewer | 90 days |
| AI Tools | AI Architect | 60 days |
| CI Pipeline | Maintainer | 60 days |
| Modules / FEA Specs | Domain Engineer | 180 days |

---

## 📚 Applicable Standards & References

- **CHBDC S6-19** — Canadian Highway Bridge Design Code  
- **CSA A23.3-19** — Design of Concrete Structures  
- **CSA S16-19** — Design of Steel Structures  
- **SimpleSpan ADRs 001–006** — Internal design records  
- **IEEE 1012 / ISO 9001 Principles** — Software quality and verification guidance

---

*This document is living governance. It evolves with the system — always reflecting the latest structure, standards, and AI collaboration protocols.*