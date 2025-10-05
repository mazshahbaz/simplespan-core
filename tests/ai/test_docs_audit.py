import subprocess
import textwrap
from datetime import date


def run(cmd, cwd="."):
    return subprocess.run(cmd, cwd=cwd, shell=True, text=True, capture_output=True)


def test_docs_audit_strict_missing_last_reviewed(tmp_path):
    # Create a temp doc without last_reviewed
    d = tmp_path / "docs" / "framework" / "tmp"
    d.mkdir(parents=True, exist_ok=True)
    md = d / "bad.md"
    md.write_text(textwrap.dedent("""
    ---
    title: Bad Doc
    version: 1.0
    context: tmp/bad
    ai_context: true
    ---
    # Bad Doc
    content
    """), encoding="utf-8")
    # Run audit in strict mode limited to this file
    cmd = (
        f"python tools/docs_audit.py --report {tmp_path}/report.json --strict --only "
        f"{md.as_posix()}"
    )
    res = run(cmd)
    assert res.returncode != 0, "Audit should fail strict mode for missing last_reviewed"


def test_docs_audit_strict_ok(tmp_path):
    d = tmp_path / "docs" / "framework" / "tmp"
    d.mkdir(parents=True, exist_ok=True)
    md = d / "ok.md"
    today = date.today().strftime("%Y-%m-%d")
    md.write_text(textwrap.dedent(f"""
    ---
    title: OK Doc
    version: 1.0
    context: tmp/ok
    last_reviewed: {today}
    ai_context: true
    ---
    # OK Doc
    content
    """), encoding="utf-8")
    cmd = (
        f"python tools/docs_audit.py --report {tmp_path}/report.json --strict --only "
        f"{md.as_posix()}"
    )
    res = run(cmd)
    assert res.returncode == 0, res.stderr