# SimpleSpan AI Router (YAML-backed)
- Map: `tools/ai/router-map.yaml` (validated by `tools/ai/router-map.schema.json`)
- CLI:
  - `--show-routes` list known routes
  - `--check` validate map + schema
  - `--list-context` print resolved context (no prompt)
  - `--dry-run` print prompt only
  - `--type/--subtype/--goal` normal generation

Examples:
```
python tools/ai/route_task.py --show-routes
python tools/ai/route_task.py --check
python tools/ai/route_task.py --type plan --subtype feature --goal "moving-load envelopes"
```