#!/usr/bin/env python3
"""
SimpleSpan AIC Logger (stub)
Appends a session log YAML file under reports/ai/sessions/ using the agreed schema.
No external dependencies required.
"""
import argparse, os, sys
from datetime import datetime, timezone
from pathlib import Path
import uuid

ALLOWED_ROLES = {"aic","planner","implementer","reviewer","auditor","human"}
ALLOWED_STATUS = {"draft","pending","accepted","rejected"}

def iso_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    p = argparse.ArgumentParser(description="Append a SimpleSpan AIC session log (YAML).")
    p.add_argument("--role", required=True, help="aic|planner|implementer|reviewer|auditor|human")
    p.add_argument("--status", required=True, help="draft|pending|accepted|rejected")
    p.add_argument("--phase", type=int, required=True, help="current phase integer")
    p.add_argument("--plan", required=True, help="path to active plan file")
    p.add_argument("--summary", required=True, help="short action summary")
    p.add_argument("--actor", default="GPT-5", help="actor identity, e.g., GPT-5, Claude, Human")
    p.add_argument("--ccp", default="", help="optional CCP tag")
    args = p.parse_args()

    role = args.role.strip().lower()
    status = args.status.strip().lower()
    if role not in ALLOWED_ROLES:
        print(f"Invalid role: {role}. Allowed: {sorted(ALLOWED_ROLES)}", file=sys.stderr); sys.exit(2)
    if status not in ALLOWED_STATUS:
        print(f"Invalid status: {status}. Allowed: {sorted(ALLOWED_STATUS)}", file=sys.stderr); sys.exit(2)

    # Prepare paths
    out_dir = Path("reports/ai/sessions")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate ID and filename
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    counter = uuid.uuid4().hex[:6].upper()
    session_id = f"AIC-{date_str}-{counter}"
    out_file = out_dir / f"{session_id}.yaml"

    # Compose YAML (minimal valid schema subset)
    yaml = []
    yaml.append(f"session_id: {session_id}")
    yaml.append(f"timestamp: {iso_now()}")
    yaml.append(f"actor: {args.actor}")
    yaml.append(f"role: {role}")
    yaml.append(f"phase: {args.phase}")
    yaml.append(f"plan_file: {args.plan}")
    yaml.append(f"action_summary: \"{args.summary}\"")
    yaml.append(f"status: {status}")
    if args.ccp:
        yaml.append(f"ccp_reference: {args.ccp}")

    content = "\n".join(yaml) + "\n"
    out_file.write_text(content, encoding="utf-8")

    print(f"Wrote session log: {out_file}")

if __name__ == "__main__":
    main()
