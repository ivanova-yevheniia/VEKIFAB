# Roller Conveyor

Reusable industrial asset. Gravity/powered roller conveyor segment for moving product between stations.

| Field | Value |
|-------|-------|
| Asset ID | `roller_conveyor` |
| Version | 1.0.0 |
| Category | material_handling |
| Tags | conveyor, roller, transport, transfer |
| Typical size | 0.5-3.0 m length, 0.5 m width, belt top 0.45 m |
| Unity collider | Box (static frame) + Box (belt plane) |
| LOD importance | medium (repeated along the line) |
| Performance budget | ~1.5k tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `roller_conveyor`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
