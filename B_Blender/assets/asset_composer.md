# Asset Composer — Assembling Stations from Reusable Assets

This document defines how **stations are assembled only by instantiating assets**
from the Industrial Asset Library. It contains **no Blender geometry and no
Python**. This stage is the industrial asset platform and its composition model.

---

## The idea

Previously a station was described by one large hand-authored parameter file.
From now on a station is nothing more than a **bill of asset instances**: a list
of "place asset *X* here, with these overrides, connected to *Y*". Each asset in
`assets/` is a self-contained, versioned, reusable module that already carries its
own geometry parameters, materials, colliders, physics and Unity tags.

```
Assets (this library)  ──▶  Station Composition (a bill of instances)  ──▶  Procedural build
   reusable modules            "place asset X at T, override P"            existing pipeline
```

The composer's only job is to **expand a composition into the procedural
grammar** the existing `procedural_builder/` already consumes — it does not draw
anything itself.

---

## What an asset provides

Every asset folder has the identical structure:

| File | Role in composition |
|------|--------------------|
| `parameters.json` | Tunable `parameters` (with defaults) + a self-contained `components` node tree at local origin `[0,0,0]`, plus the material subset it needs. |
| `assembly.json` | The asset's internal build order (root → parts → finalize). |
| `builder.json` | The **manifest**: `entry_object`, `connections` (sockets), `collider`, `physics`, `lod`, `performance_budget`, Unity tags. This is what the composer reads to place and wire the asset. |
| `design.md` | Human design intent (13 sections). |
| `README.md` | Quick facts + usage. |
| `preview.png` | Placeholder thumbnail. |

`asset_registry.json` is the index: which assets exist, their version, category,
tags, dependencies and typical usage.

---

## Station composition format

A station becomes a small **composition document** (data only). Proposed schema:

```jsonc
{
  "schema_version": "1.0",
  "station": {
    "id": "S01",
    "name": "STATION_01_Loading",
    "world_position_m": [2.5, 6.0, 0.0],   // from factory_description.json
    "front_axis": "+Y", "flow_axis": "+X"
  },
  "instances": [
    {
      "instance_id": "bench_frame_01",
      "asset": "aluminium_profile",         // registry id
      "version": "^1.0.0",                  // semver constraint
      "transform": { "position_m": [-0.85, -0.9, 0.43], "rotation_deg": [0,0,0], "scale": 1.0 },
      "parameters": { "length_m": 0.86, "section_mm": 40 },  // overrides asset defaults
      "name_prefix": "STATION_01_Loading_Leg_1"              // maps asset objects into station namespace
    },
    { "instance_id": "foot_01",  "asset": "adjustable_foot", "transform": { "position_m": [-0.85,-0.9,0.0] } },
    { "instance_id": "estop_01", "asset": "emergency_stop",  "transform": { "position_m": [-1.30,-0.88,1.20] } },
    { "instance_id": "info_01",  "asset": "information_panel","transform": { "position_m": [0.0, 2.6, 0.0] },
      "parameters": { "wrap_chars": 28 } }
    // ... one entry per physical asset in the station
  ],
  "connections": [
    { "from": "conveyor_01.out", "to": "S02:conveyor_in", "type": "transfer" }
  ]
}
```

Rules:
- **`asset`** must exist in `asset_registry.json`; **`version`** must satisfy the
  registry entry (semver).
- **`transform`** places the asset's local origin into station-local space
  (which is itself placed by `station.world_position_m`).
- **`parameters`** override only the keys the asset exposes; everything else uses
  the asset defaults.
- **`name_prefix`** renames the asset's objects into the station's Unity
  namespace (e.g. asset `PROFILE_Beam` → `STATION_01_Loading_Leg_1`), preserving
  the `STATION_*/PHYS_*/COLLIDER_*/TRIGGER_*/INFO_*` conventions.
- **`connections`** wire asset sockets (from `builder.json.connections`) to each
  other or to neighbouring stations (conveyor in/out, fence gate, cable ends).

---

## How the composer expands a composition (conceptual)

For each instance, in order:

1. **Resolve** the asset from the registry; check the version constraint and its
   `dependencies`.
2. **Load** the asset's `parameters.json`; apply the instance `parameter`
   overrides to produce concrete component values.
3. **Transform** the asset's `components` from local origin to the instance
   `transform`, then into station space.
4. **Rename** the produced objects using `name_prefix` (and the asset's own
   naming where no prefix is given).
5. **Merge materials**: the asset's `material_library` keys are unioned into one
   shared station palette — identical keys are reused, never duplicated (the
   whole line stays within the ≤16-material rule from `industrial_rules.json`).
6. **Emit** the merged result as a single station `*_parameters.json` +
   `*_assembly.json` in exactly the grammar the existing `procedural_builder`
   already reads.

The composer therefore produces the **same artifacts** that were previously
hand-authored — so `procedural_builder/builder.py` builds the station unchanged.
No new Blender code, no new station logic: **stations become data compositions of
assets.**

```
composition.json ──(composer)──▶ <station>_parameters.json + <station>_assembly.json
                                          │
                                          ▼
                             procedural_builder/builder.py  (unchanged)
                                          │
                                          ▼
                          exports/{blend,glb,screenshots}/<station>.*
```

---

## Connections & sockets

Each asset declares named sockets in `builder.json.connections` (e.g. the roller
conveyor's `in`/`out`, the fence's `post_end`/`gate`, the profile's `end_a`/
`end_b`/`face_slot`). Compositions wire sockets:

- **Frame assembly** — profiles snap `end_a`↔`end_b`; feet attach at profile
  `end` sockets; panels attach on `face_slot`.
- **Line flow** — a conveyor's `out` connects to the next station's `in`, matched
  against the conveyor coordinates in `factory_description.json`.
- **Safety** — fence bays couple `post_end`↔`post_end`; one panel is swapped for
  an interlocked gate near the walkway.

Connections are validated (both ends exist, axes are compatible) before build.

---

## Validation (reuses `procedural_builder/validation.py`)

Before a composition is built the composer checks:

- every `asset` id exists in the registry and the **version** matches;
- all instance **dependencies** are present;
- **parameter overrides** reference only keys the asset exposes and stay within
  their declared ranges/options;
- **connections** resolve on both ends with compatible axes;
- after expansion, the standard static + runtime checks run (unknown component
  types, missing materials, duplicate names, parent/dependency loops,
  overlapping bounding boxes, missing transforms) exactly as today.

---

## Worked example — rebuilding existing stations as compositions

- **S01 Loading** = `aluminium_profile` ×N (frame) + `adjustable_foot` ×4 +
  `roller_conveyor` ×1 + `plastic_parts_bin` ×N + `cardboard_box` ×8 +
  `pallet` ×2 + `electrical_cabinet` ×1 + `hmi_panel` ×1 + `emergency_stop` ×1 +
  `stack_light` ×1 + `task_light` ×1 + `cable_chain` ×1 + `information_panel` ×1
  + safety floor markings.
- **S02 Assisted Assembly** = the same frame kit + `plastic_parts_bin` ×4 +
  `hmi_panel` ×1 + `task_light` ×1 + `emergency_stop` ×1 + pump product mockups +
  `roller_conveyor` ×2 (in/out) + `information_panel` ×1.
- **S03 Robot Cell** (future) = frame kit + `safety_fence` ×several bays (with one
  gate) + `stack_light` + `emergency_stop` + `electrical_cabinet` + robot asset
  (to be added) + `information_panel`.

Each is just a different **bill of the same assets** — no new geometry code.

---

## Adding capability

- **New station** → author a new composition document only. No Python.
- **New reusable part** → add a new asset folder with the identical six-file
  structure and register it in `asset_registry.json`. It is then available to
  every station.
- **Restyle the line** → edit the shared material palette once; all assets and
  stations follow.

---

## Guarantees

- Stations are **pure data compositions** of versioned assets.
- Assets are **independent and uniform** (same six files, same manifest fields).
- The composer only **expands to the existing procedural grammar** — Blender
  remains a generic renderer and is never told what a "station" is.
- Materials are **shared and de-duplicated**; naming and Unity handoff follow the
  established conventions.

*Next stage (out of scope here): implement the composer expansion and author the
first station composition documents (S01, S02) against this library.*
