# Aluminium Profile

Reusable industrial asset. Structural aluminium slot-profile extrusion — the universal framing member.

| Field | Value |
|-------|-------|
| Asset ID | `aluminium_profile` |
| Version | 1.0.0 |
| Category | structure |
| Tags | frame, extrusion, slot-profile, structural |
| Typical size | 0.1-6.0 m length, 40x40 mm section |
| Unity collider | Box (static) |
| LOD importance | high (most repeated element in the plant) |
| Performance budget | ~200 tris (24 without slot detail) |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `aluminium_profile`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
