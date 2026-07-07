# Electrical Cabinet

Reusable industrial asset. Powder-coated electrical control enclosure with door and power indicator.

| Field | Value |
|-------|-------|
| Asset ID | `electrical_cabinet` |
| Version | 1.0.0 |
| Category | electrical |
| Tags | cabinet, enclosure, electrical, control |
| Typical size | 600x400x800 mm |
| Unity collider | Box (static) |
| LOD importance | medium |
| Performance budget | ~600 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `electrical_cabinet`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
