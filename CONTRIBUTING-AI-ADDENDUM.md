# AI Workflow Quickstart (Addendum)

**Plan**
```bash
python tools/ai/route_task.py --type plan --subtype module --goal "<goal>" --agent "Claude"
```

**Execute**
- Follow the acceptance checklist in the prompt
- Use SI units; cite CHBDC/CSA where needed

**Review**
```bash
python tools/docs_audit.py --strict --check-links --check-ai-logs
```

**Summarize (optional local check)**
```bash
python tools/ai/ai_summary.py --month $(date +'%Y-%m') --out reports/ai --csv
```

**Update AI Log Outputs Later (if needed)**
```bash
python tools/ai/ai_log_append.py --date YYYY-MM-DD --outputs docs/x.md src/y.py --reviewed-by "Reviewer"
```