# composer — Factory Composer (demo layer)

Assembles the complete MF-IP-100 production line as a **bill of asset instances**
drawn from the industrial asset library (`../assets/`). It composes data only —
**no Blender geometry is generated here**.

## Files
- `factory_composition.json` — the whole line: 7 stations, conveyor connections,
  avatar walkway, info-panel locations, safety zones, export paths.
- `station_compositions/S0*_*.json` — one bill per station; each instance has
  `asset_id`, `instance_id`, `position`, `rotation`, `scale`,
  `parameter_overrides`, `name_prefix`, `socket_connections`, `unity_tags`,
  `physics_role`.
- `factory_composer.py` — loads and resolves the composition; exposes metrics and
  integrity checks used by the Review and Report layers.

## Data flow
```
assets/ (library)  +  factory_description.json (layout)
        │
        ▼
station_compositions/*.json  ──▶  factory_composition.json
        │
        ▼
factory_composer.py  ──▶  resolved instances + metrics
        │
        ├──▶ review/factory_review.py    (validation, score)
        └──▶ reports/generate_demo_report.py (demo metrics)
```

Station instance positions are **station-local** (relative to
`station.world_position_m`); the composer resolves them to world space.

## Run
```bash
python factory_composer.py
```
Prints station/instance counts, conveyor and avatar-route lengths, integrity
checks and asset-category coverage. Standard library only; deterministic; no
Blender required.

## Next stage (not in this layer)
A composer *expansion* step would translate these instances into the procedural
grammar (`../parametric_specs` style) so `../procedural_builder/builder.py` can
render the full line. This layer stops at the composition + metrics.
