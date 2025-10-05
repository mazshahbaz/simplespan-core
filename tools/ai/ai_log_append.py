#!/usr/bin/env python3
"""Append/patch outputs and reviewer to the last ai-log entry for a given date.
Usage:
  python tools/ai/ai_log_append.py --date YYYY-MM-DD --outputs path1 path2 ... --reviewed-by "Name"
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Append outputs/reviewer to ai-log entry")
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--outputs", nargs="*", default=[], help="Paths to add to 'outputs'")
    ap.add_argument("--reviewed-by", dest="reviewed_by", help="Reviewer name to set/update")
    ap.add_argument("--logdir", default="ai-log", help="ai-log directory (default: ai-log)")
    args = ap.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except Exception:
        print("Invalid --date (expected YYYY-MM-DD)", file=sys.stderr)
        sys.exit(2)

    log_path = Path(args.logdir) / f"{args.date}.jsonl"
    lines = []
    if log_path.exists():
        lines = [ln for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    else:
        print(f"[ai_log_append] No log file for {args.date}; creating a new one", file=sys.stderr)

    # Choose the last entry or create a stub
    if lines:
        try:
            entry = json.loads(lines[-1])
        except Exception:
            print("[ai_log_append] Last log line is invalid JSON; cannot patch", file=sys.stderr)
            sys.exit(1)
    else:
        entry = {
            "timestamp": f"{args.date}T00:00:00Z",
            "agent": "TBD",
            "route": {"type":"unknown","subtype":"unknown"},
            "goal": "manual-append",
            "context_files": [],
            "prompt_file": "",
            "outputs": [],
            "decisions": [],
            "reviewed_by": "TBD",
            "version_linked": "TBD",
            "fallback": False,
            "elapsed_sec": None
        }

    # Update outputs (idempotent)
    outs = entry.get("outputs") or []
    for p in args.outputs:
        if p not in outs:
            outs.append(p)
    entry["outputs"] = outs

    # Update reviewer
    if args.reviewed_by:
        entry["reviewed_by"] = args.reviewed_by

    # Write back: replace last line or create new file
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as f:
        if lines[:-1]:
            for ln in lines[:-1]:
                f.write(ln.strip() + "\n")
        f.write(json.dumps(entry) + "\n")

    print(f"[ai_log_append] Updated {log_path}")

if __name__ == "__main__":
    main()