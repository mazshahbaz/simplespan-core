---
title: AI Development SOP — SimpleSpan
version: 1.0
context: ai/ai-development-sop
last_reviewed: 2025-10-05
ai_context: true
status: SUPERSEDED
superseded_by: ai-workflow-guide.md
---

# ⚠️ SUPERSEDED DOCUMENT

**This document has been superseded by**: [`ai-workflow-guide.md`](ai-workflow-guide.md)

**Reason**: Consolidated all AI workflow documentation into a single operational guide for clarity and ease of use.

**Date Superseded**: 2025-10-05

Please use the new consolidated guide for all AI development work.

---

# AI Development SOP — SimpleSpan (ARCHIVED)

## 1. Purpose and Scope
This Standard Operating Procedure (SOP) defines the approved process for all AI-assisted software development within the **SimpleSpan Structural Suite**.  
It applies to any contribution—code, documentation, or validation—generated or modified with AI assistance (Claude, Cursor, GPT-5, or others).

This SOP ensures every AI-generated artifact is:
- Planned and reviewed under controlled routing.
- Traceable through `ai-log/`.
- Audited by governance tools (`docs_audit.py`, `ai_summary.py`).
- Compliant with SI/CHBDC/CSA standards.

**Applies to:**
- All planning and scaffolding sessions (`plan/module`, `plan/feature`).
- Documentation, ADRs, or design reports written by AI.
- Code modules or libraries generated from prompts.

---

## 2. Development Lifecycle (Mandatory Sequence)

### **Step 1 — Plan**
Use the AI Router to create a planning prompt and context package:
```bash
python tools/ai/route_task.py --type plan --subtype module --goal "Section Properties v0.1 Planning" --agent "Claude"
```
- Ensure `.ai/context-files.txt` and `.ai/last_prompt.txt` are generated.
- Verify acceptance checklist items in the prompt.
- Confirm that all references to ADRs and framework docs resolve.

### **Step 2 — Execute**
Run the implementation or documentation phase guided by the plan.
- Follow the prompt’s **acceptance checklist** precisely.
- Apply SI units and CHBDC/CSA provisions in calculations or doc text.
- Add YAML front-matter to all generated Markdown docs.
- Mark each AI-generated file with:
  ```yaml
  ai_generated: true
  ```

### **Step 3 — Review**
A human engineer must review all AI-created artifacts.
- Run:
  ```bash
  python tools/docs_audit.py --strict --check-links --check-ai-logs
  ```
- Verify:
  - Front-matter completeness (`title`, `version`, `context`, `last_reviewed`).
  - Proper version and changelog updates.
  - References to CHBDC/CSA or SI unit consistency.
- Reviewer updates `reviewed_by` in the corresponding AI log entry.

### **Step 4 — Merge**
Merge is permitted only when:
- All CI workflows pass (router lint, docs audit, tests).
- No stale docs (`last_reviewed` within review interval).
- CHANGELOG entry documents the change.
- AI log entry includes the new file paths in `outputs`.

### **Step 5 — Audit**
Each merge triggers automated auditing:
- `docs_audit.py` verifies documentation integrity.
- `ai_summary.py` aggregates monthly AI activity metrics.
- Both results appear in CI artifacts (`docs_audit_report.json`, `ai-summary-YYYY-MM.md`).

### **Step 6 — Monthly Summary**
On the first of each month:
- `ai_summary.py` generates reports under `reports/ai/`.
- Governance review confirms review rates, fallback usage, and missing logs.

---

## 3. Required Deliverables Per AI Session
Each AI-assisted task must produce:
1. **Prompt File:** from router (e.g., `plan_module.prompt.md`).
2. **Context File List:** `.ai/context-files.txt`.
3. **Outputs:** code, documentation, or validation artifacts.
4. **Front-Matter:** standardized YAML in all Markdown docs.
5. **Tests:** validation or regression coverage.
6. **CHANGELOG.md:** updated if behavior, schema, or domain changed.
7. **AI Log Entry:** JSONL record containing:
   ```json
   {
     "timestamp": "...",
     "agent": "Claude",
     "route": {"type": "plan", "subtype": "module"},
     "goal": "Section Properties v0.1 Planning",
     "outputs": ["docs/...md", "src/...py"],
     "reviewed_by": "EngineerName"
   }
   ```

---

## 4. Review Checklist (Human Reviewer)
Before merge, confirm:
- [ ] SI units and CHBDC/CSA references applied correctly  
- [ ] Front-matter keys complete and valid  
- [ ] Tests and validation data included  
- [ ] Doc audit passes with `--strict`  
- [ ] CHANGELOG updated  
- [ ] AI log entry created/updated  
- [ ] No unresolved warnings in CI  

---

## 5. Common Mistakes to Avoid
- Missing or incomplete `ai-log` entry  
- Forgetting `ai_generated: true` in front-matter  
- Skipping the router (causes prompt/context mismatch)  
- Stale `last_reviewed` dates leading to audit warnings  
- Committing unverified generated text without human review  
- Overly large context (>150 files) — split sessions instead  

---

## 6. Governance Integration
| Tool | Function |
|------|-----------|
| **router-map.yaml** | Defines valid AI routes and context sources. |
| **route_task.py** | Generates prompts, context lists, and AI-log entries. |
| **docs_audit.py** | Validates docs, front-matter, and SI/CHBDC compliance. |
| **ai_summary.py** | Produces monthly governance reports. |
| **ADR-001** | Defines SI and metric standards. |
| **ADR-004** | Defines domain granularity for modules. |

Governance audits must pass all three checks to maintain project compliance.

---

## 7. Review & Maintenance
- Reviewed every **90 days** or after any major AI process change.
- Updated versions must increment `version:` in front-matter.
- `last_reviewed` updated by reviewer on each validation.
- Changes to this SOP must be logged in both:
  - `CHANGELOG.md`
  - `ai-summary` for the month of revision.

---

*This SOP is binding for all contributors and AI agents operating within the SimpleSpan software ecosystem.*