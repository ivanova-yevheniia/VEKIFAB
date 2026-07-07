# Cardboard Box

Reusable industrial asset. Kraft cardboard shipping carton (RSC).

| Field | Value |
|-------|-------|
| Asset ID | `cardboard_box` |
| Version | 1.0.0 |
| Category | logistics |
| Tags | box, carton, product, load |
| Typical size | 400x300x300 mm (variable) |
| Unity collider | Box (dynamic) |
| LOD importance | low |
| Performance budget | ~60 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `cardboard_box`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
