# SimpleSpan Core

**SimpleSpan Software** — Python-based structural engineering framework (SI units, CHBDC/CSA focused), optimized for AI coding agents (Cursor, Claude).

## Repository Pillars

- `src/` – Core libraries (math, geometry, materials, units), domain modules, infrastructure, apps, and presentation layers
- `tests/` – Unit, integration, validation, regression test suites
- `data/` – Materials DBs, section libraries, validation datasets, templates
- `docs/` – AI-optimized documentation framework (governance, architecture, coding standards, validation)
- `examples/` – Tutorials and example workflows
- `scripts/` – Build, linting, validation automation
- `.github/workflows/` – CI pipelines

## Quick Start (Dev)

```bash
# (optional) create virtual env
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install in editable mode
pip install -e ".[dev]"
```

## Philosophy
- Correctness > Maintainability > Performance
- Transparent engineering assumptions with CHBDC/CSA citations
- Strict SI units internally; convert at interfaces only
- Test-driven + validation against code examples
- Modular, layered architecture ready for AI assistants