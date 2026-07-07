# review — Factory Review (demo layer)

Validates the composed factory (`../composer/`) against engineering rules and
produces a scored report. Standard library only; deterministic; **no Blender
required**.

## Files
- `review_rules.json` — checks, weights (sum 100), required stations, safety
  assets, naming prefixes, clearances.
- `factory_review.py` — runs the checks and writes the report.
- `factory_review_report.md` / `.json` — generated output.

## Checks
1. Every station has an information panel
2. Every station has at least one safety-related asset
3. Material flow connected S01 → S07
4. Conveyors connect adjacent stations
5. Avatar walkway exists and does not intersect station footprints
6. Emergency stop exists where required
7. Physics objects are tagged
8. Colliders/triggers/info named per convention
9. No duplicate instance ids
10. No missing asset references
11. No obvious overlapping station footprints

## Output
A **score 0–100** (weighted), per-check `pass` / `warn` / `fail`, warnings, and
recommended improvements — written to `factory_review_report.md` and
`factory_review_report.json`.

## Run
```bash
python factory_review.py
```
