# Stack Light

Reusable industrial asset. Three-segment red/amber/green signal tower for station status.

| Field | Value |
|-------|-------|
| Asset ID | `stack_light` |
| Version | 1.0.0 |
| Category | safety |
| Tags | signal, stack-light, status, andon |
| Typical size | Ø 60 mm, 0.25-0.3 m tall |
| Unity collider | Box (static) |
| LOD importance | low |
| Performance budget | ~500 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `stack_light`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
