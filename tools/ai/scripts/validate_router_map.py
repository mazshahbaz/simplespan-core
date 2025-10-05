#!/usr/bin/env python3
# Validate router-map.yaml against schema and check prompt/context existence.
import argparse
import json
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Validate router map and generate a report")
    ap.add_argument("--map", required=True, help="Path to tools/ai/router-map.yaml")
    ap.add_argument("--schema", required=True, help="Path to tools/ai/router-map.schema.json")
    ap.add_argument("--report", default="router-map-report.json", help="Where to write JSON report")
    ap.add_argument(
        "--strict-context",
        dest="strict_context",
        action="store_true",
        help="Fail if context files/dirs are missing (Phase B)",
    )
    args = ap.parse_args()

    root = Path.cwd()
    map_path = root / args.map
    schema_path = root / args.schema

    errors = []
    warnings = []
    summary = {"routes": 0, "missing_prompts": 0, "missing_context": 0}

    # Load YAML
    try:
        import yaml  # type: ignore
    except Exception:
        print("PyYAML is required. pip install pyyaml", file=sys.stderr)
        sys.exit(2)
    try:
        data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"YAML parse failed for {args.map}: {e}")
        return finish(args.report, errors, warnings, summary)

    # Validate schema
    try:
        from jsonschema import Draft7Validator  # type: ignore
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        v = Draft7Validator(schema)
        v_errors = sorted(v.iter_errors(data), key=lambda e: e.path)
        for e in v_errors:
            path = "/".join([str(p) for p in e.path])
            errors.append(f"Schema error at {path}: {e.message}")
    except Exception as e:
        errors.append(f"Schema validation failed to run: {e}")
        return finish(args.report, errors, warnings, summary)

    if errors:
        return finish(args.report, errors, warnings, summary)

    # Token sanity
    (data.get("defaults") or {})
    routes = (data.get("routes") or {})
    summary["routes"] = sum(len(v or {}) for v in routes.values())

    allowed_tokens = {"@common"}
    for t, subs in routes.items():
        for s, body in (subs or {}).items():
            # acceptance tokens
            for item in (body.get("acceptance") or []):
                if isinstance(item, str) and item.startswith("@") and item not in allowed_tokens:
                    errors.append(
                        f"Unknown acceptance token in {t}/{s}: '{item}' (allowed: @common)"
                    )

            # prompt existence
            pr = root / (body.get("prompt") or "")
            if not pr.exists():
                summary["missing_prompts"] += 1
                errors.append(f"Missing prompt file for {t}/{s}: {body.get('prompt')}")

            # context existence (warnings in Phase A)
            for ctx in (body.get("context") or []):
                p = root / ctx
                if not p.exists():
                    summary["missing_context"] += 1
                    msg = f"Missing context path for {t}/{s}: {ctx}"
                    if args.strict_context:
                        errors.append(msg)
                    else:
                        warnings.append(msg)

    return finish(args.report, errors, warnings, summary)


def finish(report_path, errors, warnings, summary):
    status = "ok"
    if errors:
        status = "error"
    elif warnings:
        status = "warn"

    report = {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
    }
    Path(report_path).write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Print a compact console summary
    print(
        f"[router-map] status={status} routes={summary.get('routes')} "
        f"missing_prompts={summary.get('missing_prompts')} "
        f"missing_context={summary.get('missing_context')}"
    )

    if errors:
        for e in errors:
            print(f"[router-map][ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    else:
        for w in warnings:
            print(f"[router-map][WARN] {w}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()