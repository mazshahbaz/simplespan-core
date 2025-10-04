---
title: Framework Overview
version: 1.0
brand: SimpleSpan Software
context: framework/overview
audience: structural_engineers, software_engineers, ai_agents
---

© 2025 SimpleSpan Software. All rights reserved.

# SimpleSpan Framework Documentation (Overview)

This folder contains the **governance, architecture, coding, and validation** standards for **SimpleSpan Core** — a Python-based structural engineering framework using **SI units** and aligned with **Canadian codes (CHBDC/CSA)**. Documents are written to be **AI-agent friendly** (Cursor/Claude).

## Structure
```
docs/framework/
├─ 1-governance/
│  ├─ software-development-handbook.md        # Governing principles (already in repo)
│  ├─ software-architecture-guide.md          # Architecture & module design
│  └─ coding-implementation-standards.md      # Python coding standards
└─ 2-validation/
   └─ validation-verification-manual.md       # Verification & validation process
```

## How to Use (Humans & AI)
- **Humans:** Read *Handbook* → *Architecture Guide* → *Coding Standards* → *Validation Manual*.
- **AI Agents (Cursor/Claude):** Load these as context when generating code, tests, or docs.

## Key Conventions
- **Units:** SI (N, kN, m, mm, MPa, kN·m). Convert only at boundaries.
- **Codes:** CHBDC CSA S6-19, CSA A23.3-19, CSA S16-19.
- **Layers:** Presentation → Application → Domain → Infrastructure → Core.