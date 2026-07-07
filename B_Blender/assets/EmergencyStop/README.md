# Emergency Stop

Reusable industrial asset. Red mushroom emergency-stop button on a yellow backing plate.

| Field | Value |
|-------|-------|
| Asset ID | `emergency_stop` |
| Version | 1.0.0 |
| Category | safety |
| Tags | safety, e-stop, control, interactive |
| Typical size | 160x160 mm plate, Ø 40 mm button |
| Unity collider | Box (static) |
| LOD importance | medium (interactive, close inspection) |
| Performance budget | ~300 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `emergency_stop`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
