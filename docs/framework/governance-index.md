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
| **Architecture Guide** | [`software-architecture-guide.md`](1-governance/software-architecture-guide.md) | 5-layer architecture and module design |
| **Coding Standards** | [`coding-implementation-standards.md`](1-governance/coding-implementation-standards.md) | Language, style, naming, testing, modular rules |
| **Validation Manual** | [`validation-verification-manual.md`](2-validation/validation-verification-manual.md) | V&V process and testing strategy |
| **Decision Records** | [`adrs/`](1-governance/adrs/) | Immutable ADRs (001–006) for key system decisions |
| **Active Plan** | [`simple-span-framework-refinement-plan-v5.0.md`](1-governance/simple-span-framework-refinement-plan-v5.0.md) | Current framework roadmap |
| **Governance Index (this doc)** | `governance-index.md` | Table of contents for all policies and processes |

---

## 3. Framework Documentation Layers

| Layer | Description | Primary Artifacts |
|--------|--------------|-------------------|
| **1. Governance** | Standards, ADRs, policies, and collaboration protocols | `/docs/framework/1-governance/` |
| **2. Validation** | Testing philosophy, verification methods, benchmarks | `/docs/framework/2-validation/` |
| **3. Libraries** | Shared schemas, materials, section definitions | `/docs/framework/3-libraries/` |
| **4. Execution** | Prompt templates, AI tooling, CI pipelines | `/docs/framework/4-execution/` |
| **AI Framework** | AI orchestration, schemas, workflows | `/docs/framework/ai/` |

**Note**: Module-specific and FEA documentation will be created under `/docs/modules/<module>/` as domains are implemented.

```
[Governance & Architecture]
    ↓
[Validation & Testing]
    ↓
[Shared Libraries] → [AI Framework]
    ↓
[Domain Modules (future)]
```

---

## 4. AI Governance Ecosystem

| Component | File/Directory | Function |
|------------|----------------|-----------|
| **AI Workflow Guide** | [`ai/ai-workflow-guide.md`](ai/ai-workflow-guide.md) | Operational guide for all AI development work |
| **AI Router** | [`tools/ai/route_task.py`](../../tools/ai/route_task.py) | Classifies requests → emits prompts, context, and acceptance checklists |
| **Router Map** | [`tools/ai/router-map.yaml`](../../tools/ai/router-map.yaml) | Declarative route configuration |
| **Plan Schema** | [`ai/plan-schema.md`](ai/plan-schema.md) | Structure specification for roadmap documents |
| **Logging Schema** | [`ai/logging-schema.md`](ai/logging-schema.md) | AI session recording format and validation |
| **AIC Sub-Project** | [`ai/aic-subproject/`](ai/aic-subproject/) | AI Coordinator orchestration system |
| **Progress Tracking** | [`../../reports/progress.md`](../../reports/progress.md) | Session log and milestone tracking |
| **CI Workflows** | [`.github/workflows/`](../../.github/workflows/) | Automated docs audit, AI summary, tests |
| **Audit Tools** | [`tools/docs_audit.py`](../../tools/docs_audit.py) | Documentation validation and link checking |

---

## 5. Human + AI Contribution Flow

```
[Plan]
  ↓
[Execute]
  ↓
[Review]
  ↓
[Merge]
  ↓
[Audit]
  ↓
[Monthly Summary]
```

| Phase | Responsible | Tools / Prompts |
|--------|-------------|----------------|
| **Plan** | AI + Engineer | `tools/ai/route_task.py --type plan` |
| **Execute** | AI | Follow acceptance checklist from plan |
| **Review** | Human + CI | `tools/docs_audit.py`, pytest, CI workflows |
| **Merge** | Maintainer | Version bump + CHANGELOG update |
| **Audit** | Automated | Schema validation, link checking |
| **Summary** | Monthly | `tools/ai/ai_summary.py` → monthly reports |

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
| **Architecture** | `software-architecture-guide.md`, ADR-002 | N/A | 180 days |
| **Coding Style & Tests** | `coding-implementation-standards.md`, ADR-006 | CI | 180 days |
| **AI Collaboration** | `ai-workflow-guide.md`, ADR-005 | `route_task.py`, `docs_audit.py` | 90 days |
| **Versioning** | ADR-003 | `docs_audit.py` | 90 days |
| **SI Units** | ADR-001 | Code reviews | Permanent |
| **Domain Modules** | ADR-004 | Module planning | 180 days |
| **Validation Strategy** | `validation-verification-manual.md`, ADR-006 | pytest | 180 days |

---

## 8. Change and Version Policy

- **Versioning:** Semantic Versioning per ADR-003
- **Changelog:** Every merge that alters functionality must update `CHANGELOG.md`
- **AI Logging:** AI sessions logged in `reports/progress.md` per logging-schema.md
- **Review:** Governance docs reviewed every **90 days**, technical docs every **180 days**
- **Active Plan:** v5.0 (`simple-span-framework-refinement-plan-v5.0.md`)
- **Archived Plans:** v4.0 moved to `1-governance/archive/`

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