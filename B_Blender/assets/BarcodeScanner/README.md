# Barcode Scanner

Reusable industrial asset. Fixed-mount industrial barcode / code reader.

| Field | Value |
|-------|-------|
| Asset ID | `barcode_scanner` |
| Version | 1.0.0 |
| Category | sensor |
| Tags | scanner, barcode, sensor, traceability |
| Typical size | 80x60x50 mm |
| Unity collider | Box (static) |
| LOD importance | low |
| Performance budget | ~250 tris |

## Files
- `design.md` — full design specification (13 sections)
- `parameters.json` — tunable parameters + component node grammar
- `assembly.json` — ordered build operations
- `builder.json` — asset manifest (entry object, sockets, collider, LOD)
- `preview.png` — placeholder preview

## Usage
Instantiated by the asset composer (see `../asset_composer.md`) by ID `barcode_scanner`.
Override its parameters, then place/rotate per the station layout. It carries its
own materials, colliders and Unity tags — no per-station code is required.
