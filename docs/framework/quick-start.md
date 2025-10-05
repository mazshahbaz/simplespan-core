---
title: Quick Start — SimpleSpan Development Workflow
version: 1.0
context: framework/quick-start
last_reviewed: 2025-10-05
ai_generated: true
---

# 🚀 Quick Start — SimpleSpan Development Workflow

Welcome to **SimpleSpan**, the modular structural-engineering framework for CHBDC / CSA-compliant analysis and design.  
This guide explains *how to start working effectively* — whether you’re a human engineer or an AI assistant.

---

## 1️⃣ Setup Checklist

Prepare your environment:

```
- Python 3.11 or newer
- Git + GitHub access
- Cursor or Claude project configured
- Required Python libs:  pyyaml, jsonschema
```

Optional:
```bash
pip install -r requirements.txt
```

Once ready, open the repository in Cursor or your IDE.

---

## 2️⃣ Development Workflow

```
+---------+      +-----------+      +------------+      +----------+
|  Plan   | ---> |  Execute  | ---> |  Review    | ---> |  Merge   |
+---------+      +-----------+      +------------+      +----------+
                         ↓
                    [Audit & Summarize]
```

| Phase | Goal | Key Command |
|--------|------|-------------|
| **Plan** | Define task scope and deliverables | `python tools/ai/route_task.py --type plan --subtype feature --goal "FEA moving-load envelopes"` |
| **Execute** | Generate code, tests, docs via AI | `python tools/ai/route_task.py --type module --goal "section_properties v0.1 scaffold"` |
| **Review** | Validate results using CI + human check | `python tools/docs_audit.py` |
| **Merge** | Commit, update `CHANGELOG.md`, push PR | `git commit -m "Add validated module"` |
| **Audit** | Log AI outputs and produce summaries | `python tools/ai/ai_summary.py` |

---

## 3️⃣ AI Collaboration Protocol (Essentials)

1. **Always route through the AI Router** — never prompt manually without context.  
2. **Attach context files** from `.ai/context-files.txt` before each session.  
3. **Use correct prompt type:**  
   - `plan_module.prompt.md` for domain modules  
   - `plan_feature.prompt.md` for individual features  
4. **Include YAML front-matter** with `ai_generated: true` in any AI-created file.  
5. **Log everything:** add file paths to `/ai-log/YYYY-MM-DD.jsonl`.  
6. **Don’t merge** until CI passes the AI compliance check.

---

## 4️⃣ Golden Rules

✅ Use **SI units** everywhere.  
✅ Cite **CHBDC / CSA** clauses where relevant (in module docs).  
✅ Keep dependencies one-directional (no upward imports).  
✅ Update **CHANGELOG** for any behavioral or schema change.  
✅ Treat every AI output as *draft until reviewed*.  
✅ Keep your branch in sync with `main`.

---

## 5️⃣ Quick Reference Commands

```bash
# Generate planning prompt
python tools/ai/route_task.py --type plan --subtype module --goal "section_properties"

# Validate documentation and links
python tools/docs_audit.py

# Run AI compliance and produce summary
python tools/ai/ai_summary.py
```

---

## 6️⃣ Learn More

| Topic | Reference |
|--------|------------|
| Full Framework Map | [governance-index.md](governance-index.md) |
| AI Collaboration Rules | [ai-response-protocol.md](../ai-response-protocol.md) |
| Coding Standards | [1-governance/coding-implementation-standards.md](1-governance/coding-implementation-standards.md) |
| Change Policy | [change-management-policy.md](../change-management-policy.md) |
| Decision Records | [decisions/](../decisions/) |

---

*SimpleSpan development follows a disciplined Plan → Execute → Review → Merge → Audit cycle.  
Stay consistent, log every AI contribution, and keep governance synchronized.*