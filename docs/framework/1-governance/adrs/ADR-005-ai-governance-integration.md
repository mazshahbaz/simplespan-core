---
title: ADR-005 — AI Governance Integration
version: 1.0
context: governance/adrs
last_reviewed: 2025-10-05
status: Accepted
decision_date: 2025-10-05
---

# ADR-005: AI Governance Integration

## Status
**Accepted** — 2025-10-05

## Context
SimpleSpan is designed as an **AI-native framework** where AI agents (Cursor, Claude, GPT) collaborate with human engineers to develop structural engineering software. Without governance, AI outputs can be:
- Inconsistent with engineering standards
- Poorly documented or untraceable
- Difficult to audit or validate
- Unpredictable in quality

We need a system that enables AI productivity while maintaining professional engineering accountability.

## Decision
**Implement a governed AI collaboration framework with mandatory workflows, schemas, and audit trails.**

### Core Components:

#### 1. AI Coordinator (AIC)
A meta-orchestration layer that:
- Parses human intent into structured tasks
- Routes tasks to specialized AI agents
- Validates outputs against schemas
- Records all AI sessions
- Enforces guardrails and safety limits

#### 2. Multi-Agent Roles
| Role | Responsibility | Outputs |
|------|----------------|---------|
| **Planner** | Create structured plans and designs | Planning documents, interfaces |
| **Implementer** | Write code following plans | Source code, tests |
| **Reviewer** | Validate compliance and quality | Review reports, checklists |
| **Auditor** | Verify CCPs and governance | Audit reports, metrics |

#### 3. Mandatory Workflow (6-Step Cycle)
```
Plan → Execute → Review → Merge → Audit → Monthly Summary
```

Each step has:
- **Input requirements** (context documents)
- **Acceptance criteria** (checklists)
- **Output schemas** (YAML front-matter, logging format)
- **Human approval gates** (review, merge)

#### 4. Guardrails
- **File limits**: ≤12 files per AI session
- **Line limits**: ≤600 lines of code changes per session
- **Path allowlist**: AI can only modify approved directories
- **Stop rules**: Halt after 2 consecutive CI failures
- **Schema validation**: All outputs must pass schema checks

#### 5. Traceability Requirements
Every AI-generated artifact must:
- Include YAML front-matter with `ai_generated: true`
- Reference the plan or task that created it
- Log session details in `reports/progress.md`
- Link to acceptance criteria
- Update CHANGELOG.md

### AI Router (`tools/ai/route_task.py`)
Central task classifier that:
- Takes `--type` (plan/module/feature) and `--goal`
- Loads appropriate context documents
- Generates prompts with acceptance checklists
- Ensures AI has required framework context

### Schema Specifications:
- **Plan Schema** (`plan-schema.md`): Structure for roadmap documents
- **Logging Schema** (`logging-schema.md`): Session recording format
- **Front-matter Schema**: Required YAML metadata for all docs

## Rationale
1. **Accountability**: Human engineers remain responsible, AI is tool
2. **Traceability**: Every line of AI code linked to intent and validation
3. **Quality**: Schemas and checklists enforce standards
4. **Reproducibility**: Sessions can be audited and recreated
5. **Safety**: Guardrails prevent runaway changes
6. **Learning**: Metrics enable continuous improvement

## Consequences

### Positive:
- AI can safely generate large amounts of code
- All outputs auditable and traceable
- Standards enforced automatically
- Human review focused on engineering correctness
- CCPs provide cryptographic verification
- Metrics track AI effectiveness over time

### Negative:
- Overhead of planning and logging
- Learning curve for AI collaboration workflow
- Must maintain schemas and tools
- Cannot skip governance steps

### Mitigations:
- Automate as much as possible (router, validators)
- Provide templates and examples
- Make workflow tools easy to use
- Document AI collaboration clearly
- Show value through successful module delivery

## Implementation Requirements

### Phase 1 — Foundation (Complete):
- ✅ AI Router (`route_task.py`)
- ✅ Plan schema specification
- ✅ Progress tracking (`progress.md`)
- ✅ Basic logging structure

### Phase 2 — Operational (In Progress):
- ⚪ AIC Orchestrator operational
- ⚪ Schema validators in CI
- ⚪ Guardrail enforcement
- ⚪ Complete logging schema
- ⚪ Review templates

### Phase 3 — Advanced (Planned):
- ⚪ Multi-agent handoffs
- ⚪ Automated CCP creation
- ⚪ Metrics dashboard
- ⚪ Learning feedback loops

## Acceptance Checklist for AI Outputs:
Every AI-generated artifact must satisfy:
- [ ] SI units; CHBDC/CSA inline where applicable
- [ ] Front-matter present; `ai_generated: true`
- [ ] Validation artifacts (tests or JSON cases) included
- [ ] Cross-links to ADRs and framework docs
- [ ] AI log entry created and `CHANGELOG.md` updated
- [ ] Interfaces documented with typed signatures
- [ ] Human review completed and approved

## Governance Metrics:
Track monthly:
- Number of AI sessions
- Lines of code generated
- Pass rate (CI success on first try)
- Review acceptance rate
- Schema compliance rate
- Average session duration

## Human Responsibilities:
1. **Intent Definition**: Provide clear goals and context
2. **Plan Approval**: Review and approve AI-generated plans
3. **Code Review**: Verify engineering correctness
4. **Merge Approval**: Final gate before integration
5. **CCP Verification**: Validate continuity checkpoints

## AI Responsibilities:
1. **Context Loading**: Load all required framework docs
2. **Schema Compliance**: Follow YAML front-matter requirements
3. **Standards Adherence**: SI units, CHBDC/CSA citations
4. **Logging**: Record session details
5. **Testing**: Generate tests with validation cases
6. **Documentation**: Update docs and changelog

## Related Decisions
- ADR-001: SI Units (AI must use SI internally)
- ADR-002: Layer Architecture (AI respects layer boundaries)
- ADR-003: Semantic Versioning (AI updates versions properly)
- ADR-004: Domain Granularity (AI plans within module boundaries)
- ADR-006: Testing and Validation Strategy (AI generates tests)

## References
- `docs/framework/ai/ai-workflow-guide.md` — Operational guide (supersedes SOP and bootstrap)
- `docs/framework/ai/plan-schema.md` — Planning document structure
- `docs/framework/ai/logging-schema.md` — Session logging format
- `tools/ai/route_task.py` — AI task router
- SimpleSpan Whitepaper v1.0 (agentic engineering model)
