# AIC Orchestrator Bundle — 2025-10-05

This bundle installs the local CLI coordinator for your Agent-in-Command (AIC).

## Files
- `tools/aic_orchestrator.py` — read-only v1. Loads v4.0 plan, reads resume_context, prints next tasks.

## Install
Unzip at the **repo root** (same level as `docs/`, `tools/`, etc.).

## Usage
```bash
python tools/aic_orchestrator.py
python tools/aic_orchestrator.py --json
python tools/aic_orchestrator.py --phase 3 --max-tasks 2
python tools/aic_orchestrator.py --strict
```

## Notes
- Expects: `docs/framework/1-governance/simple-span-framework-refinement-plan-v4.0.md`
- Optional: `reports/progress.md`
- No writes, no dependencies. Safe to run in CI (read-only).
