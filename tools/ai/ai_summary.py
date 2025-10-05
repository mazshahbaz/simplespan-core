#!/usr/bin/env python3
"""AI Activity Summary Generator
Aggregates /ai-log/*.jsonl entries into monthly JSON/Markdown (and optional CSV).

Usage:
  python tools/ai/ai_summary.py --month 2025-10 --out reports/ai --csv --strict
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ADR_RE = re.compile(r"ADR-\d{3}")


def month_from_ts(ts: str) -> str:
    try:
        # Accept '2025-10-05T12:34:56Z' or '2025-10-05 12:34:56'
        ts = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m")
    except Exception:
        try:
            dt = datetime.strptime(ts[:10], "%Y-%m-%d")
            return dt.strftime("%Y-%m")
        except Exception:
            return "unknown"


def normalize_entry(raw: dict) -> dict:
    route = raw.get("route") or {}
    rtype = route.get("type") or "unknown"
    rsub = route.get("subtype") or "unknown"
    goal = raw.get("goal") or ""
    ctx = raw.get("context_files") or []
    outs = raw.get("outputs") or []
    agent = raw.get("agent") or "TBD"
    reviewed_by = raw.get("reviewed_by") or "TBD"
    ts = raw.get("timestamp") or ""
    month = month_from_ts(ts)
    # risks/signals inferred
    has_outputs = bool(outs)
    fallback_used = bool(raw.get("fallback", False))  # future-proof; router can set it later
    # decisions may include ADR references
    adrs: list[str] = []
    for d in raw.get("decisions") or []:
        if isinstance(d, dict):
            for v in d.values():
                if isinstance(v, str):
                    adrs += ADR_RE.findall(v)
        elif isinstance(d, str):
            adrs += ADR_RE.findall(d)
    return {
        "timestamp": ts,
        "month": month,
        "route_type": rtype,
        "route_subtype": rsub,
        "goal": goal,
        "context_len": len(ctx),
        "outputs": outs,
        "has_outputs": has_outputs,
        "agent": agent,
        "reviewed_by": reviewed_by,
        "reviewed": reviewed_by not in (None, "", "TBD"),
        "fallback_used": fallback_used,
        "adrs": sorted(set(adrs)),
    }


def load_month_logs(log_dir: Path, month: str):
    records = []
    if not log_dir.exists():
        return records
    # read only files that start with YYYY-MM
    for p in sorted(log_dir.glob(f"{month}-*.jsonl")):
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except Exception:
                continue
            rec = normalize_entry(raw)
            # if timestamp missing month, map by filename's month
            if rec["month"] == "unknown":
                rec["month"] = month
            if rec["month"] == month:
                records.append(rec)
    return records


def pct(n, d):
    return 0.0 if d == 0 else round(100.0 * n / d, 1)


def summarize(records):
    N = len(records)
    with_outputs = sum(1 for r in records if r["has_outputs"]) 
    reviewed = sum(1 for r in records if r["reviewed"]) 
    fallbacks = sum(1 for r in records if r["fallback_used"]) 
    avg_ctx = round(sum(r["context_len"] for r in records) / N, 1) if N else 0.0

    # group by route
    routes = defaultdict(list)
    for r in records:
        routes[(r["route_type"], r["route_subtype"])].append(r)
    by_route = []
    for (t, s), items in sorted(routes.items()):
        m = len(items)
        by_route.append({
            "type": t,
            "subtype": s,
            "sessions": m,
            "with_outputs_pct": pct(sum(1 for x in items if x["has_outputs"]), m),
            "reviewed_pct": pct(sum(1 for x in items if x["reviewed"]), m),
            "avg_ctx": round(sum(x["context_len"] for x in items) / m, 1) if m else 0.0,
        })

    # by agent
    agents = defaultdict(list)
    for r in records:
        agents[r["agent"]].append(r)
    by_agent = []
    for a, items in sorted(agents.items()):
        m = len(items)
        by_agent.append({
            "agent": a,
            "sessions": m,
            "reviewed_pct": pct(sum(1 for x in items if x["reviewed"]), m),
            "avg_outputs": round(sum(len(x["outputs"]) for x in items) / m, 2) if m else 0.0,
        })

    # by reviewer
    reviewers = defaultdict(list)
    for r in records:
        reviewers[r["reviewed_by"]].append(r)
    by_reviewer = []
    for rv, items in sorted(reviewers.items()):
        if rv in (None, "", "TBD"):
            continue
        by_reviewer.append({"reviewer": rv, "sessions": len(items)})

    # risks
    risks = {
        "no_outputs": [
            r["timestamp"] + " — " + (r["goal"] or "")
            for r in records
            if not r["has_outputs"]
        ],
        "no_reviewer": [
            r["timestamp"] + " — " + (r["goal"] or "")
            for r in records
            if not r["reviewed"]
        ],
        "fallback_routes": [
            r["timestamp"] + " — " + (r["goal"] or "")
            for r in records
            if r["fallback_used"]
        ],
        "large_context": [
            r["timestamp"] + f" — ctx={r['context_len']} — " + (r["goal"] or "")
            for r in records
            if r["context_len"] > 150
        ],
    }

    # files and adrs
    files_created = sorted({p for r in records for p in (r["outputs"] or [])})
    adrs = Counter(a for r in records for a in r["adrs"])

    summary = {
        "counts": {
            "sessions": N,
            "with_outputs": with_outputs,
            "reviewed": reviewed,
            "fallback_est": fallbacks,
            "avg_ctx": avg_ctx,
        },
        "by_route": by_route,
        "by_agent": by_agent,
        "by_reviewer": by_reviewer,
        "risks": risks,
        "files_created": files_created,
        "adrs_touched": sorted(adrs.keys()),
    }
    return summary


def write_json(out_dir: Path, month: str, data: dict):
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"ai-summary-{month}.json"
    data = {"month": month, "generated_at": datetime.utcnow().isoformat() + "Z", **data}
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return p


def write_md(out_dir: Path, month: str, data: dict):
    p = out_dir / f"ai-summary-{month}.md"
    c = [f"# AI Activity Summary — {month}", ""]
    counts = data["counts"]
    sessions = counts["sessions"]
    with_outputs_pct = 0 if sessions == 0 else round(100 * counts["with_outputs"] / sessions, 1)
    reviewed_pct = 0 if sessions == 0 else round(100 * counts["reviewed"] / sessions, 1)
    c += [
        "## Overview",
        f"- Sessions: {sessions}",
        f"- With outputs: {counts['with_outputs']} ({with_outputs_pct}%)",
        f"- Reviewed: {counts['reviewed']} ({reviewed_pct}%)",
        f"- Fallback estimate: {counts['fallback_est']}",
        f"- Avg context size: {counts['avg_ctx']} files",
        "",
    ]
    # By Route
    c += [
        "## By Route",
        "| type | subtype | sessions | outputs % | reviewed % | avg ctx |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for r in data["by_route"]:
        row = (
            f"| {r['type']} | {r['subtype']} | {r['sessions']} | "
            f"{r['with_outputs_pct']} | {r['reviewed_pct']} | {r['avg_ctx']} |"
        )
        c.append(row)
    c.append("")

    # Risks
    risks = data["risks"]
    c += ["## Risks"]
    c.append(f"- No outputs: {len(risks['no_outputs'])}")
    c.append(f"- No reviewer: {len(risks['no_reviewer'])}")
    c.append(f"- Fallback routes: {len(risks['fallback_routes'])}")
    c.append(f"- Large context (>150 files): {len(risks['large_context'])}")
    c.append("")
    if risks["no_outputs"]:
        c.append("**No outputs (examples):**\n- " + "\n- ".join(risks["no_outputs"][:10]))
        c.append("")
    if risks["no_reviewer"]:
        c.append("**No reviewer (examples):**\n- " + "\n- ".join(risks["no_reviewer"][:10]))
        c.append("")

    # Files Created
    files = data.get("files_created", [])
    c += ["## Files Created/Updated"]
    if files:
        c += ["- " + "\n- ".join(files[:100])]
    else:
        c += ["(none)"]
    c.append("")

    # ADRs
    adrs = data.get("adrs_touched", [])
    c += ["## ADRs Referenced"]
    if adrs:
        c += ["- " + "\n- ".join(adrs)]
    else:
        c += ["(none)"]

    p.write_text("\n".join(c), encoding="utf-8")
    return p


def write_csv(out_dir: Path, month: str, records: list):
    p = out_dir / f"ai-summary-{month}.csv"
    fields = [
        "timestamp",
        "route_type",
        "route_subtype",
        "agent",
        "reviewed_by",
        "has_outputs",
        "fallback_used",
        "context_len",
        "goal",
    ]
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            w.writerow({k: r.get(k) for k in fields})
    return p


def main():
    ap = argparse.ArgumentParser(description="AI monthly summary generator")
    ap.add_argument("--month", help="YYYY-MM (default = current UTC month)")
    ap.add_argument("--logs", default="ai-log", help="Path to ai-log directory")
    ap.add_argument("--out", default="reports/ai", help="Output directory for reports")
    ap.add_argument("--csv", action="store_true", help="Also write CSV export")
    ap.add_argument("--strict", action="store_true", help="Exit 1 if risk thresholds exceeded")
    ap.add_argument(
        "--threshold",
        type=float,
        default=20.0,
        help="Max % unreviewed allowed in strict mode (default 20%)",
    )
    args = ap.parse_args()

    # Determine month
    now = datetime.utcnow()
    month = args.month or now.strftime("%Y-%m")

    log_dir = Path(args.logs)
    out_dir = Path(args.out)

    records = load_month_logs(log_dir, month)
    if not records:
        print(f"[ai_summary] No logs found for {month} in {log_dir}")
        sys.exit(2)

    data = summarize(records)
    json_p = write_json(out_dir, month, data)
    md_p = write_md(out_dir, month, data)
    if args.csv:
        csv_p = write_csv(out_dir, month, records)
        print(
            f"[ai_summary] Wrote {json_p} \n[ai_summary] Wrote {md_p} \n[ai_summary] Wrote {csv_p}"
        )
    else:
        print(f"[ai_summary] Wrote {json_p} \n[ai_summary] Wrote {md_p}")

    # Strict mode: fail if unreviewed exceeds threshold
    unreviewed = data["counts"]["sessions"] - data["counts"]["reviewed"]
    sessions = data["counts"]["sessions"]
    unrev_pct = 0.0 if sessions == 0 else 100.0 * unreviewed / sessions
    if args.strict and unrev_pct > args.threshold:
        msg = (
            f"[ai_summary] STRICT FAIL: {unrev_pct:.1f}% unreviewed > "
            f"{args.threshold:.1f}% threshold"
        )
        print(msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()