# HMI Panel

Reusable industrial asset. Operator HMI / guidance touchscreen with bezel and hardware buttons.

| Field | Value |
|-------|-------|
| Asset ID | `hmi_panel` |
| Version | 1.0.0 |
| Category | control |
| Tags | hmi, touchscreen, control, guidance |
| Typical size | 300x220 mm active area, ~15-22 inch class |
| Unity collider | Box (static) |
| LOD importance | medium |
| Performance budget | ~400 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `hmi_panel`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
