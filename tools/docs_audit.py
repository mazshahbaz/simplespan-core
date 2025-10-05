#!/usr/bin/env python3

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED_KEYS = ["title", "version", "context", "last_reviewed"]
OPTIONAL_KEYS = ["ai_generated", "ai_context"]

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
# Allow optional leading whitespace/newlines before front-matter
FRONT_MATTER_PATTERN = re.compile(r"^\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def load_yaml(text):
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except Exception:
        # Fallback: minimal front-matter parser for simple key: value pairs
        fm = {}
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val
        return fm

def parse_markdown(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    fm = {}
    body = text
    m = FRONT_MATTER_PATTERN.match(text)
    if m:
        fm_text = m.group(1)
        try:
            fm = load_yaml(fm_text) or {}
        except Exception as e:
            fm = {"_yaml_error": str(e)}
        body = text[m.end():]
    # headings and links
    headings = []
    for line in body.splitlines():
        if line.lstrip().startswith("#"):
            headings.append(line.strip())
    links = LINK_PATTERN.findall(body)
    return fm, body, headings, links

def semverish(v: str) -> bool:
    return bool(re.match(r"^\d+\.\d+(\.\d+)?$", str(v).strip()))

def parse_date(s: str):
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%Y/%m/%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None

def bucket_for(path: Path, cfg) -> str:
    p = path.as_posix()
    if not cfg:
        return "default"
    paths = (cfg.get("paths") or {})
    for bucket, globs in paths.items():
        for g in globs or []:
            if Path(p).match(g):
                return bucket
    # heuristics
    if "/ai/" in p or "ai-response-protocol" in p:
        return "ai"
    if "/1-governance/" in p or "change-management-policy" in p:
        return "governance"
    if "/6-fea/" in p:
        return "fea"
    if "/5-modules/" in p:
        return "modules"
    if "/3-libraries/" in p:
        return "libraries"
    return "default"

def max_days_for(bucket: str, cfg) -> int:
    default = 180
    if not cfg:
        return default
    rev = cfg.get("review_intervals") or {}
    return int(rev.get(bucket, default))

def build_summary_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]

def iter_docs(root: Path, only_glob=None, since=None):
    # If an absolute file path is provided, yield it directly if it exists
    if only_glob:
        og_path = Path(str(only_glob))
        if og_path.is_absolute() and og_path.exists() and og_path.suffix.lower() == ".md":
            yield og_path
            return

    for p in root.rglob("*.md"):
        if ".venv" in p.parts or "node_modules" in p.parts:
            continue
        if only_glob:
            posix = p.as_posix()
            # Allow glob match, exact absolute match, or basename match
            if not (
                Path(posix).match(only_glob)
                or posix == only_glob
                or posix.endswith("/" + only_glob)
            ):
                continue
        if since:
            if datetime.date.fromtimestamp(p.stat().st_mtime) < since:
                continue
        yield p

def load_ai_logs(ai_log_dir: Path):
    logs = []
    if ai_log_dir.exists():
        for p in ai_log_dir.glob("*.jsonl"):
            try:
                for line in p.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    logs.append(json.loads(line))
            except Exception:
                continue
    return logs

def file_in_ai_logs(path: Path, logs):
    posix = path.as_posix()
    for entry in logs:
        outs = entry.get("outputs") or []
        if isinstance(outs, list) and any(posix in str(x) for x in outs):
            return True
        # allow match by context or prompt_file for now (lenient)
        if posix == (entry.get("prompt_file") or ""):
            return True
    return False

def main():
    ap = argparse.ArgumentParser(description="Consolidated documentation auditor")
    ap.add_argument("--root", default=".", help="Repo root")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors for key checks")
    ap.add_argument("--no-index", action="store_true", help="Skip building docs/context_index.json")
    ap.add_argument(
        "--report",
        default="docs/docs_audit_report.json",
        help="Path to write JSON report",
    )
    ap.add_argument("--since", help="Only scan files modified since YYYY-MM-DD")
    ap.add_argument("--only", help="Only scan files matching PATH/GLOB (posix)")
    ap.add_argument("--fail-on-stale", action="store_true", help="Fail if staleness exceeds limits")
    ap.add_argument("--check-links", action="store_true", help="Verify relative links exist")
    ap.add_argument(
        "--check-anchors",
        action="store_true",
        help="(Light) check anchors (best-effort)",
    )
    ap.add_argument(
        "--check-ai-logs",
        action="store_true",
        help="Verify ai_generated files are logged",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    docs_root = root / "docs"
    ai_log_dir = root / "ai-log"

    cfg_path = docs_root / "docs_audit.config.yaml"
    cfg = None
    if cfg_path.exists():
        try:
            import yaml
            cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        except Exception:
            cfg = None

    since_date = None
    if args.since:
        try:
            since_date = datetime.datetime.strptime(args.since, "%Y-%m-%d").date()
        except Exception:
            print("Invalid --since date; expected YYYY-MM-DD", file=sys.stderr)
            sys.exit(2)

    errors, warnings, stale = [], [], []
    contexts = []  # for context_index.json
    logs = load_ai_logs(ai_log_dir) if args.check_ai_logs else []

    files_scanned = 0

    for p in iter_docs(docs_root, only_glob=args.only, since=since_date):
        files_scanned += 1
        meta, body, headings, links = parse_markdown(p)

        # Front-matter required keys
        if not meta:
            msg = f"{p.as_posix()}: missing YAML front-matter"
            (errors if args.strict else warnings).append(msg)
            continue

        if "_yaml_error" in meta:
            (errors if args.strict else warnings).append(
                f"{p.as_posix()}: YAML error: {meta['_yaml_error']}"
            )

        for k in REQUIRED_KEYS:
            if k not in meta:
                (errors if args.strict else warnings).append(
                    f"{p.as_posix()}: missing front-matter key '{k}'"
                )

        # SemVer-ish
        if "version" in meta and not semverish(str(meta["version"])):
            warnings.append(f"{p.as_posix()}: version not SemVer-ish '{meta['version']}'")

        # last_reviewed date and staleness
        lr = meta.get("last_reviewed")
        d = None
        if lr:
            d = None
            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%dT%H:%M:%SZ"):
                try:
                    d = datetime.datetime.strptime(str(lr), fmt).date()
                    break
                except Exception:
                    continue
            if not d:
                (errors if args.strict else warnings).append(
                    f"{p.as_posix()}: invalid last_reviewed '{lr}'"
                )
        else:
            (errors if args.strict else warnings).append(f"{p.as_posix()}: missing last_reviewed")

        # Staleness check
        if d:
            bucket = bucket_for(p, cfg)
            max_days = max_days_for(bucket, cfg)
            age = (datetime.date.today() - d).days
            if age > max_days:
                stale.append({
                    "path": p.as_posix(),
                    "last_reviewed": str(d),
                    "age_days": age,
                    "max_days": max_days,
                })
                if args.fail_on_stale:
                    errors.append(
                        f"{p.as_posix()}: stale by {age - max_days} days (bucket={bucket})"
                    )
                else:
                    warnings.append(
                        f"{p.as_posix()}: stale by {age - max_days} days (bucket={bucket})"
                    )

        # AI log compliance
        if args.check_ai_logs and meta.get("ai_generated") is True:
            if not file_in_ai_logs(p, logs):
                (errors if args.strict else warnings).append(
                    f"{p.as_posix()}: ai_generated true but no ai-log entry found"
                )

        # Link checks (basic)
        if args.check_links:
            for link in links:
                if "://" in link or link.startswith("#"):
                    continue
                # trim anchors
                target = link.split("#")[0]
                target_path = (p.parent / target).resolve()
                if not target_path.exists():
                    (errors if args.strict else warnings).append(
                        f"{p.as_posix()}: broken link -> {link}"
                    )

        # Build context index entry
        # Normalize potentially non-JSON-serializable types (e.g., date)
        lr_val = meta.get("last_reviewed")
        lr_str = str(lr_val) if lr_val is not None else None
        ver_val = meta.get("version")
        ver_str = str(ver_val) if ver_val is not None else None

        contexts.append({
            "path": p.as_posix(),
            "title": meta.get("title"),
            "version": ver_str,
            "last_reviewed": lr_str,
            "ai_context": bool(meta.get("ai_context")),
            "headings": headings[:50],
            "links": links[:100],
            "summary_hash": hashlib.sha256(
                (meta.get("title", "") + "\n" + "\n".join(headings)).encode("utf-8")
            ).hexdigest()[:16],
        })

    # Write context index unless suppressed
    if not args.no_index:
        idx_path = docs_root / "context_index.json"
        idx_path.parent.mkdir(parents=True, exist_ok=True)
        idx_path.write_text(
            json.dumps(
                {"generated": datetime.datetime.utcnow().isoformat() + "Z", "files": contexts},
                indent=2,
            ),
            encoding="utf-8",
        )

    # Report
    status = "ok"
    if errors:
        status = "error"
    elif stale or warnings:
        status = "warn"

    report = {
        "status": status,
        "summary": {
            "files": files_scanned,
            "errors": len(errors),
            "warnings": len(warnings),
            "stale": len(stale),
        },
        "errors": errors,
        "warnings": warnings,
        "stale": stale,
    }

    # Ensure report directory exists
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Console summary
    print(
        f"[docs_audit] status={status} files={files_scanned} errors={len(errors)}"
        f" warnings={len(warnings)} stale={len(stale)}"
    )
    if errors:
        for e in errors:
            print(f"[docs_audit][ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    else:
        for w in warnings:
            print(f"[docs_audit][WARN] {w}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
