# reports — Factory Report (demo layer)

Generates a demo-oriented summary of the composed factory. Standard library only;
deterministic; **no Blender required**.

## Files
- `factory_metrics.py` — collects Blender-free metrics from the Factory Composer
  and scans `../exports/` for any generated files.
- `generate_demo_report.py` — writes the report.
- `demo_report.md` / `demo_report.json` — generated output.

## Report contents
Project name, use case, product, factory area, and counts of stations, asset
instances, conveyors, info panels, physics objects, collider candidates and
trigger zones; estimated conveyor length; avatar route length; asset coverage by
category; a list of any generated/exported files; and a short explanation of the
AI pipeline:

`customer requirements → process plan → asset composition → procedural builder → Blender → Unity avatar walkthrough`

## Run
```bash
python generate_demo_report.py
```
(Optionally run `../review/factory_review.py` first so the report can include the
latest review score.)
