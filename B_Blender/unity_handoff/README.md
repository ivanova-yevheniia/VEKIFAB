# unity_handoff — WP B → WP D handoff

This is the boundary between **WP B (Blender)** and **WP D (Unity)**.

> **Architecture decision:** Blender generates **individual station prefabs only**.
> **Unity assembles the full production line and the avatar walkthrough.**
> Do **not** expect Blender to export a whole-factory scene.

## Files
- `unity_factory_layout.json` — the handoff manifest (generated).
- `generate_unity_layout.py` — builds it from `requirements/factory_description.json`,
  `reasoning/reasoning_summary.json` and the exported GLBs.

## What Unity does with `unity_factory_layout.json`

1. **Import station prefabs.** For each entry in `prefabs_to_generate`, import the
   corresponding `exports/glb/<prefab>.glb` as a prefab (one per station *type*).
   Parallel instances reuse the same prefab.
2. **Place stations.** For each `station_placements[*]`, instantiate its
   `prefab_glb` at `position_m`, `rotation_deg`, `scale` (metres, glTF Y-up,
   1 unit = 1 m).
3. **Add physics/colliders by object-name prefix** (`physics_expectations`):
   - `COLLIDER_*` → static collider (convex box), no Rigidbody
   - `PHYS_*` → Rigidbody (dynamic; kinematic if the object's `kinematic` extra is true)
   - `TRIGGER_*` → collider with `isTrigger = true` (usually no renderer)
   - `INFO_*` → UI data source
   - `CONVEYOR_*` → kinematic belt, moves product at `belt_speed_mps`
   - `STATION_*` → static structural geometry
   The glTF **extras** (`unity_tag`, `collider`, `rigidbody`, `mass`, `kinematic`,
   `is_trigger`, `station_id`) carry the exact per-object intent.
4. **Wire the info panels.** When the avatar enters a station's `trigger`
   (e.g. `TRIGGER_Info_RobotCell`), look up its `reasoning_key` in
   `reasoning/reasoning_summary.json` and show `title` / `summary` /
   `decision_tree` / `engineering_notes` / `future_improvements` on the
   `INFO_*` panel.
5. **Build the walking route.** Drive the avatar along
   `avatar_walkway.waypoints_m` (`route_length_m` is precomputed); stop at each
   `inspect` waypoint in front of a station.
6. **Connect conveyors.** Use `conveyors[*]` (`from`/`to`, `start_m`/`end_m`,
   `belt_speed_mps`) to link stations and move product along the line.

## Manifest fields
- `prefabs_to_generate` — unique station GLBs to import (+ `exists_in_exports`).
- `station_placements` — per-instance placement, trigger, info panel, reasoning
  key and `parallel_group` (set when a station is a parallel copy).
- `conveyors`, `avatar_walkway`, `info_panels`, `safety_zones`.
- `physics_expectations` — the name-prefix → behaviour contract above.

## Regenerate
```bash
python generate_unity_layout.py
```
Run after the planning → factory_description → compositions chain so the manifest
matches the current line.

## Notes
- Only station **types** need a GLB; `station_placements` may reference the same
  prefab multiple times (parallel assembly, repeated stations).
- Prefabs not yet exported are flagged `exists_in_exports: false` — generate them
  in Blender via the procedural builder before final assembly.
