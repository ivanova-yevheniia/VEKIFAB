# Task Light

Reusable industrial asset. LED task-light bar for worktop illumination.

| Field | Value |
|-------|-------|
| Asset ID | `task_light` |
| Version | 1.0.0 |
| Category | lighting |
| Tags | light, task, machine-light, led |
| Typical size | 0.8 m bar |
| Unity collider | Box (static) |
| LOD importance | low |
| Performance budget | ~200 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `task_light`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
