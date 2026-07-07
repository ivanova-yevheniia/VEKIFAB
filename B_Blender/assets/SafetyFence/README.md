# Safety Fence

Reusable industrial asset. Modular mesh safety-fence bay (posts + panels).

| Field | Value |
|-------|-------|
| Asset ID | `safety_fence` |
| Version | 1.0.0 |
| Category | safety |
| Tags | fence, guard, safety, perimeter |
| Typical size | 1.0 m bay width x 2.0 m height (repeatable) |
| Unity collider | Box per post + Box per panel |
| LOD importance | medium |
| Performance budget | ~1.2k tris per bay |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `safety_fence`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
