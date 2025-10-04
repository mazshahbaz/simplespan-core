# Contributing to SimpleSpan Core

Thank you for contributing! This project targets professional structural engineering practice (CHBDC/CSA) with SI units and AI-assisted workflows.

## Workflow Summary
1. Create an issue describing your proposal or bug.
2. Create a feature branch: `feat/<short-name>` or `fix/<short-name>`.
3. Add/modify code **and** update docs under `/docs/framework/` as needed.
4. Write tests under `/tests/` (unit + validation when applicable).
5. Submit a PR. Ensure CI checks pass (lint, type, tests, validation).

## Code Standards
- Python 3.11+
- PEP 8 + project-specific standards under `/docs/framework/1-governance/coding-implementation-standards.md`
- Docstrings: NumPy or Google style; include **units** for all physical quantities.
- No silent failures; raise explicit exceptions with actionable messages.

## Validation
For calculation modules, add a case under `/tests/validation/` referencing CHBDC/CSA examples with documented tolerances.