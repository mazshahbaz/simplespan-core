import os, sys, subprocess, json, pathlib

def run(cmd, cwd="."):
    return subprocess.run(cmd, cwd=cwd, shell=True, text=True, capture_output=True)

def test_router_dry_run_prints_prompt():
    # Ensure script exists
    assert pathlib.Path("tools/ai/route_task.py").exists(), "route_task.py missing"
    # Dry-run should print prompt to STDOUT and not write files
    res = run("python tools/ai/route_task.py --type plan --subtype module --goal \"pytest smoke\" --agent \"Claude\" --dry-run")
    assert res.returncode == 0, res.stderr
    assert "AI Task" in res.stdout
    assert "Acceptance Checklist" in res.stdout

def test_router_fallback_on_unknown_subtype():
    res = run("python tools/ai/route_task.py --type plan --subtype UNKNOWN_SUBTYPE --goal \"pytest fallback\" --agent \"Claude\" --dry-run")
    # Should still succeed and include a router warning
    assert res.returncode == 0, res.stderr
    assert "ROUTER WARNING" in res.stdout or "used fallback" in res.stderr or "used fallback" in res.stdout