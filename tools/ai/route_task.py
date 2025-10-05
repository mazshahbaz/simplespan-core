#!/usr/bin/env python3
# SimpleSpan AI Router (YAML-backed)
# Usage examples:
#   python tools/ai/route_task.py --type plan --subtype feature --goal "moving loads"
#   python tools/ai/route_task.py --show-routes
#   python tools/ai/route_task.py --check
#   python tools/ai/route_task.py --type plan --subtype module --list-context
import argparse
import datetime
import json
import os
import sys
import traceback
from pathlib import Path


def posixify(p: Path) -> str:
    try:
        return p.as_posix()
    except Exception:
        return str(p).replace(os.sep, '/')

REPO_ROOT = Path.cwd()
DEFAULT_MAP_PATH = REPO_ROOT / "tools" / "ai" / "router-map.yaml"
DEFAULT_SCHEMA_PATH = REPO_ROOT / "tools" / "ai" / "router-map.schema.json"

# Built-in fallback (minimal) to ensure router still works if YAML is bad/missing.
BUILTIN_MAP = {
    "plan": {
        "module": {
            "prompt": "docs/framework/4-execution/prompt-library/plan_module.prompt.md",
            "context": [
                "docs/framework/5-modules/module-planning-playbook.md",
                "docs/framework/5-modules/module-scaffolding-handoff-sop.md",
                "docs/framework/1-governance/coding-implementation-standards.md",
                "docs/framework/ai-response-protocol.md",
                "docs/framework/decisions/ADR-001-SI-units-and-metric.md",
                "docs/framework/decisions/ADR-004-domain-granularity.md"
            ],
            "acceptance": [
                "SI units; CHBDC/CSA inline where applicable",
                "Front-matter present; ai_generated: true (if AI-created)",
                "Validation artifacts (tests or JSON cases) included",
                "Cross-links to ADRs/framework docs",
                "Append AI-log entry and update CHANGELOG.md",
                "Interfaces documented with typed signatures",
                "Validation plan includes tolerances and sources"
            ]
        },
        "feature": {
            "prompt": "docs/framework/4-execution/prompt-library/plan_feature.prompt.md",
            "context": [
                "docs/framework/ai-response-protocol.md",
                "docs/framework/1-governance/coding-implementation-standards.md",
                "docs/framework/decisions/ADR-001-SI-units-and-metric.md",
                "docs/framework/decisions/ADR-004-domain-granularity.md"
            ],
            "acceptance": [
                "SI units; CHBDC/CSA inline where applicable",
                "Front-matter present; ai_generated: true (if AI-created)",
                "Validation artifacts (tests or JSON cases) included",
                "Cross-links to ADRs/framework docs",
                "Append AI-log entry and update CHANGELOG.md",
                "Feature constraints documented; scope and assumptions explicit"
            ]
        }
    },
    "module": {
        "_default": {
            "prompt": "docs/framework/4-execution/prompt-library/module_scaffold.prompt.md",
            "context": [
                "docs/framework/5-modules/module-planning-playbook.md",
                "docs/framework/5-modules/module-scaffolding-handoff-sop.md"
            ],
            "acceptance": [
                "Docstrings include SI units & CHBDC/CSA references",
                "Unit tests + \u22651 validation JSON case",
                "No upward imports; CI green",
                "AI log entry created"
            ]
        }
    },
    "fea": {
        "_default": {
            "prompt": "docs/framework/4-execution/prompt-library/fea_module_scaffold.prompt.md",
            "context": [
                "docs/framework/6-fea/fea-architecture-and-design.md",
                "docs/framework/6-fea/element-library-spec.md",
                "docs/framework/6-fea/loads-and-moving-loads-spec.md",
                "docs/framework/6-fea/solver-and-assembly-spec.md",
                "docs/framework/6-fea/results-and-postprocessing-spec.md"
            ],
            "acceptance": [
                "API signatures present",
                "Envelopes spec followed",
                "Station queries independent of mesh",
                "AI log entry created"
            ]
        }
    },
    "docs": {
        "_default": {
            "prompt": "docs/framework/4-execution/prompt-library/docs_update.prompt.md",
            "context": [
                "docs/framework/documentation-governance.md",
                "docs/framework/change-management-policy.md",
                "docs/framework/contributor-playbook.md"
            ],
            "acceptance": [
                "Front-matter present & valid",
                "Links and spellcheck pass",
                "CHANGELOG updated if behavior/version changed",
                "AI log entry created"
            ]
        }
    }
}

def load_yaml(path: Path):
    try:
        import yaml  # type: ignore
    except Exception:
        raise RuntimeError("PyYAML not installed. Install with: pip install pyyaml jsonschema")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def validate_schema(data: dict, schema_path: Path):
    try:
        from jsonschema import Draft7Validator  # type: ignore
    except Exception:
        raise RuntimeError("jsonschema not installed. Install with: pip install jsonschema pyyaml")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    v = Draft7Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: e.path)
    if errors:
        msgs = []
        for e in errors:
            path = "/".join([str(p) for p in e.path])
            msgs.append(f"- {path}: {e.message}")
        raise ValueError("Router Map failed schema validation:\n" + "\n".join(msgs))

def expand_acceptance_tokens(route: dict, defaults: dict):
    out = []
    common = defaults.get("acceptance_common", [])
    for item in route.get("acceptance", []):
        if item == "@common":
            if not isinstance(common, list):
                raise ValueError("defaults.acceptance_common must be a list of strings")
            out.extend(common)
        elif isinstance(item, str):
            out.append(item)
        else:
            raise ValueError("Acceptance list contains a non-string item")
    route["acceptance"] = out
    return route

def collect_context(entries):
    files = []
    for entry in entries:
        p = (REPO_ROOT / entry).resolve()
        if p.is_dir():
            for root, _, fnames in os.walk(p):
                for fn in fnames:
                    if fn.lower().endswith(".md"):
                        files.append(Path(root) / fn)
        else:
            if p.exists():
                files.append(p)
            else:
                print(f"[router] WARNING: context path not found: {entry}", file=sys.stderr)
    # Deduplicate and sort in POSIX presentation
    posix = sorted(set(posixify(Path(os.path.relpath(f, REPO_ROOT))) for f in files))
    return posix

def read_prompt_text(prompt_rel: str):
    ap = REPO_ROOT / prompt_rel
    if not ap.exists():
        return f"# MISSING PROMPT — Create {prompt_rel}"
    try:
        return ap.read_text(encoding="utf-8")
    except Exception as e:
        return f"# ERROR READING PROMPT {prompt_rel}\n{e}"

def resolve_route(yaml_map, rtype, subtype):
    warnings = []
    defaults = yaml_map.get("defaults", {}) if yaml_map else {}
    routes = yaml_map.get("routes", {}) if yaml_map else {}

    route = None
    if rtype in routes and subtype in routes[rtype]:
        route = routes[rtype][subtype]
    elif rtype in routes and "_default" in routes[rtype]:
        route = routes[rtype]["_default"]
        warnings.append(f"unknown route '{rtype}/{subtype}' — used fallback {rtype}/_default")
    elif "docs" in routes and "_default" in routes["docs"]:
        route = routes["docs"]["_default"]
        warnings.append(f"unknown route '{rtype}/{subtype}' — used fallback docs/_default")

    used_fallback = bool(warnings)
    if route is None:
        # Fallback to built-in
        bi_group = BUILTIN_MAP.get(rtype) or {}
        route = bi_group.get(subtype) or bi_group.get("_default") or BUILTIN_MAP["docs"]["_default"]
        warnings.append("router-map.yaml missing/invalid — using built-in routes")
        return route, defaults, warnings, True

    # Expand tokens
    try:
        route = expand_acceptance_tokens(dict(route), defaults)
    except Exception as e:
        warnings.append(f"token expansion error: {e}. Falling back to built-in.")
        bi_group = BUILTIN_MAP.get(rtype) or {}
        route = bi_group.get(subtype) or bi_group.get("_default") or BUILTIN_MAP["docs"]["_default"]
        return route, {}, warnings, True

    return route, defaults, warnings, used_fallback

def emit_prompt_text(route_info, goal, context_files, warnings):
    header = [
        "# AI Task",
        f"Type: {route_info['type']}/{route_info['subtype']}",
        f"Goal: {goal}",
        "",
        "## Context Files (attach these)",
    ] + [f"- {p}" for p in context_files]

    warn_block = []
    for w in warnings:
        warn_block.append(f"<!-- ROUTER WARNING: {w} -->")

    prompt_text = read_prompt_text(route_info["prompt_file"])

    accept = "\n".join([f"- [ ] {i}" for i in route_info["acceptance"]])

    parts = []
    if warn_block:
        parts.append("\n".join(warn_block))
    parts.append("\n".join(header))
    parts.append("\n## Required Prompt\n" + prompt_text)
    parts.append("\n## Acceptance Checklist\n" + accept)
    return "\n\n".join(parts)

def append_ai_log(route_info, goal, context_files):
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    log_dir = REPO_ROOT / "ai-log"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{ts[:10]}.jsonl"
    entry = {
        "timestamp": ts,
        "agent": "TBD",
        "route": {"type": route_info["type"], "subtype": route_info["subtype"]},
        "goal": goal,
        "context_files": context_files,
        "prompt_file": route_info["prompt_file"],
        "outputs": [],
        "decisions": [],
        "reviewed_by": "TBD",
        "version_linked": "TBD"
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    ap = argparse.ArgumentParser(description="SimpleSpan AI Router (YAML-backed)")
    ap.add_argument("--type", dest="rtype", help="Task type (plan, module, fea, docs)")
    ap.add_argument("--subtype", default="module", help="Subtype (module, feature, _default)")
    ap.add_argument("--goal", help="Short description of the task objective")
    ap.add_argument(
        "--outfile",
        default=".ai/last_prompt.txt",
        help="Where to write the final prompt",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print to STDOUT; do not write files or ai-log",
    )
    ap.add_argument(
        "--show-routes",
        dest="show_routes",
        action="store_true",
        help="List available routes from YAML",
    )
    ap.add_argument(
        "--list-context",
        dest="list_context",
        action="store_true",
        help="Print resolved context files (no prompt)",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Validate YAML + schema + prompt paths and exit",
    )
    ap.add_argument(
        "--map",
        default=str(DEFAULT_MAP_PATH),
        help="Path to router-map.yaml",
    )
    ap.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="Path to router-map.schema.json",
    )
    args = ap.parse_args()

    yaml_map = None

    # Load YAML map if present
    map_path = Path(args.map)
    schema_path = Path(args.schema)

    # Attempt to parse and validate YAML map
    yaml_err = None
    if map_path.exists() and schema_path.exists():
        try:
            yaml_map = load_yaml(map_path)
            validate_schema(yaml_map, schema_path)
        except Exception as e:
            yaml_err = str(e)
            print(f"[router] WARNING: {yaml_err}", file=sys.stderr)
            yaml_map = None
    else:
        if not map_path.exists():
            print(f"[router] WARNING: router map not found: {map_path}", file=sys.stderr)
        if not schema_path.exists():
            print(f"[router] WARNING: schema not found: {schema_path}", file=sys.stderr)

    # Show routes
    if args.show_routes:
        routes = yaml_map.get("routes", {}) if yaml_map else {}
        if not routes:
            print("(Using built-in map)")
            routes = BUILTIN_MAP
        for t, subs in routes.items():
            for s in subs.keys():
                print(f"{t}/{s}")
        return

    # Check mode (validate)
    if args.check:
        ok = True
        if yaml_err:
            ok = False
        if yaml_map:
            # Basic existence checks for prompt files
            routes = yaml_map.get("routes", {})
            for t, subs in routes.items():
                for s, body in subs.items():
                    pr = REPO_ROOT / body.get("prompt", "")
                    if not pr.exists():
                        print(f"[router] WARNING: prompt file missing: {body.get('prompt')}")
        sys.exit(0 if ok else 1)

    # For list-context or normal generation, we require rtype and goal
    if not args.rtype:
        print("--type is required unless using --show-routes or --check", file=sys.stderr)
        sys.exit(2)
    if not (args.goal or args.list_context):
        print(
            "--goal is required unless using --list-context/--show-routes/--check",
            file=sys.stderr,
        )
        sys.exit(2)

    # Resolve route
    route, defaults, warnings, fell_back = resolve_route(
        yaml_map or {"routes": {}}, args.rtype, args.subtype
    )

    context_files = collect_context(route.get("context", []))

    if args.list_context:
        for p in context_files:
            print(p)
        return

    # Prepare route_info for prompt assembly
    route_info = {
        "type": args.rtype,
        "subtype": args.subtype,
        "prompt_file": route.get("prompt", ""),
        "acceptance": route.get("acceptance", []),
    }

    final_prompt = emit_prompt_text(route_info, args.goal, context_files, warnings)

    if args.dry_run:
        print(final_prompt)
        return

    # Write outputs
    out_path = REPO_ROOT / args.outfile
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_prompt, encoding="utf-8")

    ctx_path = REPO_ROOT / ".ai" / "context-files.txt"
    ctx_path.parent.mkdir(parents=True, exist_ok=True)
    ctx_path.write_text("\n".join(context_files), encoding="utf-8")

    append_ai_log(route_info, args.goal, context_files)

    print("=== AI ROUTER ===")
    print(f"Wrote prompt to {posixify(out_path)}")
    print(f"Wrote context list to {posixify(ctx_path)}")
    print(f"Route: {args.rtype}/{args.subtype} {'(fallback)' if fell_back else ''}")
    if warnings:
        for w in warnings:
            print(f"[router] WARNING: {w}", file=sys.stderr)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[router] ERROR:", e, file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
