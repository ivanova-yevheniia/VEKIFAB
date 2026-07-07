# WP B — Blender Generation Workflow

This document describes the **planned** end-to-end workflow for generating a
factory production line in Blender. Nothing here generates geometry yet — it is
the roadmap the generators in `../generators/` will follow.

## Pipeline overview

```
customer_requirements.json
        │   (Claude: interpret & plan)
        ▼
production_line_plan.json
        │   (Claude: expand to layout)
        ▼
factory_description.json
        │   (Blender Python generators)
        ▼
Blender scene  (STATION_* / CONVEYOR_* / PHYS_* / COLLIDER_* / TRIGGER_* / INFO_*)
        │   (export)
        ▼
.blend  +  .glb  +  screenshots
        │   (import)
        ▼
Unity avatar walkthrough
```

## Stages in detail

### 1. `customer_requirements.json`
The raw production requirements provided by the customer: product, target
output, floor space, automation level, required operations, constraints.
Lives in `../requirements/customer_requirements.json`.

### 2. → `production_line_plan.json`
Claude interprets the requirements and produces an **ordered plan** of stations
(which station types, in which order, with which parameters) plus the conveyor
connections between them. Station types are drawn from
`../requirements/station_library.json`.

### 3. → `factory_description.json`
The plan is expanded into a complete, machine-readable **layout**: absolute
positions, rotations, dimensions, and connections for every station and
conveyor. This file is the single source of truth consumed by the generators.

### 4. → Blender Python generator
`generate_full_factory.py` loads `factory_description.json` and dispatches each
station to the matching `generate_<type>.py` generator. Shared logic (naming,
materials, colliders, triggers, transforms, export) lives in
`common_blender_utils.py`. Output objects follow the naming conventions in
`unity_import_notes.md`.

### 5. → `.blend` / `.glb` export
The finished scene is saved to:
- `../exports/blend/`  — native Blender working files
- `../exports/glb/`    — glTF exports for Unity
- `../exports/screenshots/` — preview renders

### 6. → Unity avatar walkthrough
Unity imports the `.glb`. An avatar walks the line and inspects each station.
Colliders (`COLLIDER_*`) and triggers (`TRIGGER_*`) drive interaction and
inspection; `INFO_*` objects carry metadata. See `unity_import_notes.md`.

## Regeneration principle

Each station is generated independently, so a single station can be regenerated
or tweaked without rebuilding the whole line. The full line is always
reproducible from `factory_description.json`.

## Current status

Scaffolding only. Next step: define the concrete JSON schemas and implement
`common_blender_utils.py`, then the first station generator (loading station).
