# Pallet

Reusable industrial asset. Standard wooden block pallet (EUR-class proportion).

| Field | Value |
|-------|-------|
| Asset ID | `pallet` |
| Version | 1.0.0 |
| Category | logistics |
| Tags | pallet, logistics, load-carrier, wood |
| Typical size | 1200x800x144 mm (EUR-class) |
| Unity collider | Box (static) |
| LOD importance | low |
| Performance budget | ~400 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `pallet`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
