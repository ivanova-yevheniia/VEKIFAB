# Information Panel

Reusable industrial asset. Free-standing information / signage panel with title, body and avatar trigger.

| Field | Value |
|-------|-------|
| Asset ID | `information_panel` |
| Version | 1.0.0 |
| Category | ux |
| Tags | signage, info, walkthrough, trigger |
| Typical size | 1200x700 mm board at ~1.6 m height |
| Unity collider | Box (static) + Box (trigger) |
| LOD importance | medium |
| Performance budget | ~300 tris (+ text) |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `information_panel`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
