
#!/usr/bin/env python3
"""
AIC Orchestrator (read-only v1)
--------------------------------
Reads the v4.0 plan and progress log, loads YAML resume_context, identifies the
current phase, and prints the next 1–3 unchecked checklist items with helpful
hints. Uses only the Python stdlib.

Usage:
  python tools/aic_orchestrator.py [--plan PATH] [--progress PATH]
                                   [--phase N] [--max-tasks K]
                                   [--json] [--strict]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Dict

DEFAULT_PLAN = "docs/framework/1-governance/simple-span-framework-refinement-plan-v4.0.md"
DEFAULT_PROGRESS = "reports/progress.md"

ALLOWLIST_PATHS = [
    "docs/", "tools/", "src/simplespan_", "tests/", ".github/", ".ai/", "reports/", "validation/"
]
DIFF_CAPS = {"files": 12, "lines": 600}

PHASE_TITLES = {
    0: "Repository Synchronization & Baseline",
    1: "Governance Review & Consolidation",
    2: "Schema & Goal Tag Implementation",
    3: "Governance Audit & Cross-Reference",
    4: "Automation Track 1",
    5: "Agent Pipeline",
    6: "FEA Domain Initialization",
    7: "Governance Scanner & Auto-Tasks",
    8: "Autonomous Validation & Release",
    9: "Continuous Learning Factory",
    10: "Multi-Domain Expansion",
    11: "Continuity & Context Preservation",
}

@dataclass
class ChecklistItem:
    text: str
    checked: bool

@dataclass
class Phase:
    number: int
    title: str
    checklist: List[ChecklistItem]
    anchor: str

def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def parse_resume_context(plan_text: str) -> Dict[str, str]:
    """
    Extract the fenced YAML block that contains resume_context.
    We do a light parse of 3 fields: current_phase, last_ccp, progress_file.
    """
    # find a fenced block that starts with ```yaml
    fence_re = re.compile(r"```yaml(.*?)```", re.DOTALL | re.IGNORECASE)
    for m in fence_re.finditer(plan_text):
        block = m.group(1)
        if "resume_context:" in block:
            # light parse
            ctx = {}
            # remove leading/trailing backticks leftovers
            lines = [ln.rstrip() for ln in block.splitlines()]
            current_key = None
            for ln in lines:
                # strip YAML comments
                raw = ln.split("#", 1)[0].rstrip()
                if not raw.strip():
                    continue
                # top-level simple keys we care about
                m_phase = re.search(r"\bcurrent_phase:\s*([0-9]+)\b", raw)
                if m_phase:
                    ctx["current_phase"] = int(m_phase.group(1))
                m_ccp = re.search(r"\blast_ccp:\s*(.+)$", raw)
                if m_ccp and "last_ccp" not in ctx:
                    ctx["last_ccp"] = m_ccp.group(1).strip()
                m_prog = re.search(r"\bprogress_file:\s*(.+)$", raw)
                if m_prog and "progress_file" not in ctx:
                    ctx["progress_file"] = m_prog.group(1).strip()
            return ctx
    return {}

def parse_phase_sections(plan_text: str) -> List[Phase]:
    """
    Parse Phase sections and their checklists.
    Phase header patterns:
      ## Phase N — Title
      ## Phase N - Title
    Checklist header:
      ### ✅ Checklist
    Items:
      - [x] ... or - [ ] ...
    """
    phases: List[Phase] = []

    # Normalize newlines
    text = plan_text.replace("\r\n", "\n")

    # Find all phase headers with positions
    phase_re = re.compile(r"^##\s+Phase\s+(\d+)\s+[—-]\s+(.*)$", re.MULTILINE)
    matches = list(phase_re.finditer(text))
    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]

        # Anchor approximation
        anchor = f"phase-{num}"

        # Find checklist block
        cl_header = re.search(r"^###\s+✅\s+Checklist\s*$", section, re.MULTILINE)
        checklist: List[ChecklistItem] = []
        if cl_header:
            cl_start = cl_header.end()
            # end at next ### or ##
            end_m = re.search(r"^##\s+|^###\s+", section[cl_start:], re.MULTILINE)
            cl_end = cl_start + end_m.start() if end_m else len(section)
            cl_block = section[cl_start:cl_end]
            # parse items
            for line in cl_block.splitlines():
                m_item = re.match(r"^\s*-\s*\[(x| )\]\s+(.*)$", line.strip(), re.IGNORECASE)
                if m_item:
                    checked = (m_item.group(1).lower() == "x")
                    text_item = m_item.group(2).strip()
                    checklist.append(ChecklistItem(text=text_item, checked=checked))

        phases.append(Phase(number=num, title=title, checklist=checklist, anchor=anchor))
    return phases

def determine_current_phase(resume_ctx: Dict[str, str], override_phase: Optional[int]) -> Optional[int]:
    if override_phase is not None:
        return override_phase
    return resume_ctx.get("current_phase")

def next_unchecked_items(phase: Phase, k: int) -> List[str]:
    out: List[str] = []
    for it in phase.checklist:
        if not it.checked:
            out.append(it.text)
        if len(out) >= k:
            break
    return out

def infer_candidate_paths(tasks: List[str]) -> List[str]:
    paths = set()
    for t in tasks:
        low = t.lower()
        # Heuristics
        if "governance-playbook" in low:
            paths.add("docs/framework/1-governance/governance-playbook.md")
        if "oath" in low or "charter" in low:
            paths.add("docs/framework/1-governance/oaths-and-charter.md")
        if "schema" in low:
            paths.add("tools/ai/schema_validator.py")
            paths.add("docs/framework/1-governance/")
        if "progress" in low:
            paths.add("reports/progress.md")
        if "ai prompt" in low or "prompts" in low:
            paths.add("docs/framework/ai/prompts/")
        if "release" in low:
            paths.add(".github/workflows/release.yml")
            paths.add("tools/validation_runner.py")
        if "scanner" in low:
            paths.add("tools/ai/auto_scanner.py")
            paths.add(".github/workflows/auto-scanner.yml")
        if "agent" in low:
            paths.add(".github/workflows/agent-pipeline.yml")
        if "cli" in low or "wrapper" in low or "simplespan_tools.py" in low:
            paths.add("tools/simplespan_tools.py")
        if "moving loads" in low or "fea" in low:
            paths.add("docs/framework/6-fea/")
            paths.add("src/simplespan_fea/")
            paths.add("tests/fea/")
        # Generic governance references
        if "adr" in low:
            paths.add("docs/framework/1-governance/adrs/")
    return sorted(paths)[:6]

def acceptance_hints_for_phase(n: int) -> List[str]:
    base = {
        1: [
            "Front-matter valid across governance docs",
            "Each Oath maps to at least one measurable KPI",
            "docs_audit.py --strict passes"
        ],
        2: [
            "schema_validator.py exists and validates front-matter",
            "ai logs include goal_tag and schema_version",
            "ai_summary shows Top Tags"
        ],
        3: [
            "docs_audit.py --strict --check-links returns 0 errors",
            "docs/context_index.json generated",
            "external audit summary produced"
        ],
        4: [
            "CI workflows produce reproducible PRs",
            "CLI parity with CI verified"
        ],
        5: [
            "Agent guardrails enforced at router level",
            "Human merge gate verified"
        ],
        6: [
            "Validation seeds pass for moving-loads",
            "CI green for domain tests"
        ],
        7: [
            "auto_scanner opens issues for stale docs",
            "Weekly schedule runs without errors"
        ],
        8: [
            "validation_runner produces pass ≥98%",
            "ccp-manifest.json generated & signed"
        ],
        9: [
            "≥500 agent sessions available for optimization",
            "Governance dashboard renders without errors"
        ],
        10: [
            "Second domain passes shared-core validation",
            "CI/Audit metrics steady"
        ],
        11: [
            "context_rehydrate.py loads last CCP & context index",
            "Cross-AI recovery succeeds <15 min"
        ]
    }
    return base.get(n, ["Phase acceptance criteria: see v4.0 plan section for this phase."])

def risks_for_phase(n: int) -> List[str]:
    base = {
        1: ["Link rot or duplicate content", "Unclear ownership on roles matrix"],
        2: ["Breaking existing logs with new schema", "Inconsistent versions across docs"],
        3: ["Hidden broken links", "Outdated ADR references"],
        4: ["Label misfires triggering wrong workflows", "Infinite loop triggers"],
        5: ["Guardrails too loose; excessive diffs", "Ambiguous file targets"],
        6: ["Tolerance misconfiguration for CHBDC cases", "Overfitting tests to examples"],
        7: ["Issue spam or noise", "False positives on stale detection"],
        8: ["Unsigned artifacts", "Silent validation drift"],
        9: ["Premature optimization with low data volume", "Feedback loops degrading quality"],
        10: ["Core/library coupling too tight", "Inconsistent style across domains"],
        11: ["Missing CCP manifest integrity", "Resume context drift across AIs"]
    }
    return base.get(n, ["General governance risks; apply stop conditions if unsure."])

def render_human(phase_num: int, phase_title: str, last_ccp: str, tasks: List[str]) -> str:
    cand = infer_candidate_paths(tasks)
    hints = acceptance_hints_for_phase(phase_num)
    risks = risks_for_phase(phase_num)
    lines = []
    lines.append(f"Current Phase: {phase_num} — {phase_title}")
    lines.append(f"Last CCP: {last_ccp or '—'}")
    lines.append(f"Next Tasks ({len(tasks)}):")
    for i, t in enumerate(tasks, 1):
        lines.append(f"  {i}) {t}")
    if cand:
        lines.append("Proposed Paths (edit candidates):")
        for p in cand:
            lines.append(f"  - {p}")
    lines.append("Acceptance to Verify:")
    for h in hints:
        lines.append(f"  - {h}")
    lines.append("Risks & Rollback:")
    for r in risks:
        lines.append(f"  - {r}")
    lines.append("Guardrails:")
    lines.append(f"  - Allowlist: {', '.join(ALLOWLIST_PATHS)}")
    lines.append(f"  - Diff caps: ≤ {DIFF_CAPS['files']} files, ≤ {DIFF_CAPS['lines']} lines")
    return "\n".join(lines)

def render_json(phase_num: int, phase_title: str, last_ccp: str, tasks: List[str]) -> str:
    out = {
        "phase": phase_num,
        "phase_title": phase_title,
        "last_ccp": last_ccp or None,
        "next_tasks": tasks,
        "candidate_paths": infer_candidate_paths(tasks),
        "acceptance_hints": acceptance_hints_for_phase(phase_num),
        "risks": risks_for_phase(phase_num),
        "guardrails": {
            "allowlist": ALLOWLIST_PATHS,
            "diff_caps": DIFF_CAPS
        }
    }
    return json.dumps(out, indent=2)

def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="AIC Orchestrator (read-only v1)")
    ap.add_argument("--plan", default=DEFAULT_PLAN, help="Path to v4.0 plan markdown")
    ap.add_argument("--progress", default=DEFAULT_PROGRESS, help="Path to progress log")
    ap.add_argument("--phase", type=int, default=None, help="Override current phase")
    ap.add_argument("--max-tasks", type=int, default=3, help="Number of unchecked items to return")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    ap.add_argument("--strict", action="store_true", help="Non-zero exit if required artifacts missing/invalid")
    args = ap.parse_args(argv)

    plan_path = Path(args.plan)
    if not plan_path.exists():
        msg = f"[ERROR] Plan not found: {plan_path}"
        print(msg, file=sys.stderr)
        return 2 if args.strict else 0

    try:
        plan_text = load_text(plan_path)
    except Exception as e:
        print(f"[ERROR] Failed to read plan: {e}", file=sys.stderr)
        return 2 if args.strict else 0

    resume = parse_resume_context(plan_text)
    if not resume:
        print("[WARN] resume_context not found in plan.", file=sys.stderr)
    current_phase = determine_current_phase(resume, args.phase)
    if current_phase is None:
        print("[ERROR] Unable to determine current phase (resume_context missing, and no --phase).", file=sys.stderr)
        return 3 if args.strict else 0

    phases = parse_phase_sections(plan_text)
    target: Optional[Phase] = next((p for p in phases if p.number == current_phase), None)
    if target is None:
        print(f"[ERROR] Phase {current_phase} not found in plan.", file=sys.stderr)
        return 4 if args.strict else 0

    tasks = next_unchecked_items(target, args.max_tasks)
    phase_title = target.title or PHASE_TITLES.get(current_phase, f"Phase {current_phase}")
    last_ccp = resume.get("last_ccp", "") if resume else ""

    if args.json:
        print(render_json(current_phase, phase_title, last_ccp, tasks))
    else:
        print(render_human(current_phase, phase_title, last_ccp, tasks))

    return 0

if __name__ == "__main__":
    sys.exit(main())
