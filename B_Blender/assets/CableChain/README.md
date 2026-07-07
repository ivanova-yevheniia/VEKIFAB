# Cable Chain

Reusable industrial asset. Articulated cable / energy chain (drag chain) run.

| Field | Value |
|-------|-------|
| Asset ID | `cable_chain` |
| Version | 1.0.0 |
| Category | cable_management |
| Tags | cable, energy-chain, drag-chain, routing |
| Typical size | 0.5 m run, ~50 mm link pitch |
| Unity collider | None (visual) |
| LOD importance | low |
| Performance budget | ~300 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `cable_chain`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
