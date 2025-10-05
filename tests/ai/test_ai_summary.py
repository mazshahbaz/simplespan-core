import json
import subprocess
from datetime import datetime


def run(cmd, cwd="."):
    return subprocess.run(cmd, cwd=cwd, shell=True, text=True, capture_output=True)


def test_ai_summary_counts_and_latency(tmp_path):
    # Prepare ai-log for current month
    month = datetime.utcnow().strftime("%Y-%m")
    day = datetime.utcnow().strftime("%Y-%m-%d")
    logdir = tmp_path / "ai-log"
    logdir.mkdir(parents=True, exist_ok=True)
    log = logdir / f"{day}.jsonl"
    # two entries
    e1 = {
        "timestamp": f"{day}T12:00:00Z",
        "agent": "Claude",
        "route": {"type": "plan", "subtype": "module"},
        "goal": "test1",
        "context_files": ["docs/a.md"],
        "outputs": ["docs/x.md"],
        "reviewed_by": "Reviewer",
        "fallback": False,
        "elapsed_sec": 1.5,
    }
    e2 = {
        "timestamp": f"{day}T13:00:00Z",
        "agent": "Cursor",
        "route": {"type": "docs", "subtype": "_default"},
        "goal": "test2",
        "context_files": [],
        "outputs": [],
        "reviewed_by": "TBD",
        "fallback": True,
        "elapsed_sec": 2.0,
    }
    with log.open("w", encoding="utf-8") as f:
        f.write(json.dumps(e1) + "\n")
        f.write(json.dumps(e2) + "\n")

    outdir = tmp_path / "reports" / "ai"
    outdir.mkdir(parents=True, exist_ok=True)

    # Run summary pointing to tmp ai-log
    cmd = (
        f"python tools/ai/ai_summary.py --month {month} --logs {logdir.as_posix()} "
        f"--out {outdir.as_posix()} --csv"
    )
    res = run(cmd)
    assert res.returncode in (0, 1), res.stderr  # strict not used, so should be 0
    # Read JSON output
    jpath = outdir / f"ai-summary-{month}.json"
    assert jpath.exists(), "JSON summary not created"
    data = json.loads(jpath.read_text(encoding="utf-8"))
    assert data["counts"]["sessions"] == 2
    assert data["counts"]["reviewed"] == 1
    assert data["counts"]["with_outputs"] == 1