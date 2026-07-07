# Plastic Parts Bin

Reusable industrial asset. Angled plastic small-parts / kanban bin.

| Field | Value |
|-------|-------|
| Asset ID | `plastic_parts_bin` |
| Version | 1.0.0 |
| Category | storage |
| Tags | bin, kanban, parts, storage |
| Typical size | 300x400x200 mm (size 4 class) |
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
Instantiated by the asset composer (see `../asset_composer.md`) by ID `plastic_parts_bin`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
