# Adjustable Foot

Reusable industrial asset. Levelling / anti-vibration foot for frames and machines.

| Field | Value |
|-------|-------|
| Asset ID | `adjustable_foot` |
| Version | 1.0.0 |
| Category | structure |
| Tags | foot, levelling, mounting, anti-vibration |
| Typical size | Ø 60 mm base, M12 stud, 40-120 mm height |
| Unity collider | Box (static) |
| LOD importance | low (small, seen at floor level) |
| Performance budget | ~120 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `adjustable_foot`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
