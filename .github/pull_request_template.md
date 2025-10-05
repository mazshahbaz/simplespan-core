## Summary
Describe the change and why it's needed.

## Checklist
- [ ] Used the router to generate prompts + context
  - Attached `.ai/last_prompt.txt` and `.ai/context-files.txt`
- [ ] Ran docs audit in strict mode
  - `python tools/docs_audit.py --strict --check-links --check-ai-logs`
- [ ] AI log updated
  - Includes `agent`, `outputs`, and `reviewed_by`
- [ ] CHANGELOG.md updated (if behavior/schema/docs changed)
- [ ] SI/CHBDC/CSA references included where applicable

## Notes for Reviewers
- Risks, assumptions, and validation references