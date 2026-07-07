# WP B — Unity Import Notes & Naming Conventions

These notes define how Blender output must be structured and named so it imports
cleanly into Unity for the avatar walkthrough (WP A / D). Follow these
conventions in every generator.

## Object naming conventions

All generated objects use an UPPERCASE prefix so Unity scripts can reliably find
and group them. Format: `PREFIX_<Name>` (e.g. `STATION_Assembly_01`).

| Prefix       | Meaning | Notes |
|--------------|---------|-------|
| `STATION_*`  | A production station (root of a station's hierarchy). | One per station; children parented under it. |
| `CONVEYOR_*` | A conveyor segment connecting stations. | Defines material flow between stations. |
| `PHYS_*`     | Visual / physical geometry (meshes the avatar sees). | The renderable body of a machine. |
| `COLLIDER_*` | Collision geometry for the avatar (walls, blocking volumes). | Simplified shapes; become Unity colliders. |
| `TRIGGER_*`  | Trigger volumes for interaction / inspection events. | Non-blocking; fire Unity events when the avatar enters. |
| `INFO_*`     | Metadata / annotation markers (labels, inspection points). | Carry station data for the inspection UI. |

### Examples
```
STATION_Loading_01
  PHYS_Loading_01_Body
  COLLIDER_Loading_01_Base
  TRIGGER_Loading_01_Inspect
  INFO_Loading_01_Label
CONVEYOR_01_02
```

## Hierarchy

- Each station is a single `STATION_*` empty/root with all its parts parented
  underneath (`PHYS_*`, `COLLIDER_*`, `TRIGGER_*`, `INFO_*`).
- Conveyors (`CONVEYOR_*`) are top-level or grouped separately, linking stations
  by their ids.

## Transforms & units

- **Units:** meters (Blender scene unit = 1 m). Matches Unity's 1 unit = 1 m.
- **Up axis:** export glTF with **Y-up** for Unity (`+Y up`, `-Z forward`).
- **Apply transforms** (scale = 1, rotation applied) before export.
- **Origin:** place each station's origin at its footprint center on the floor
  (z = 0) for predictable placement in Unity.

## Export settings (glTF / .glb)

- Format: `.glb` (binary, self-contained) into `../exports/glb/`.
- Include: meshes, materials, empties (for `STATION_*`/`INFO_*` markers),
  custom properties (for metadata).
- Colliders and triggers exported as simple mesh volumes; Unity converts them to
  Mesh/Box colliders and `isTrigger` volumes based on the prefix.

## Metadata

`INFO_*` objects (and optionally custom properties on `STATION_*`) should carry:
station id, station type, and any inspection text the Unity UI displays during
the walkthrough.

## Status

Conventions defined; generators not yet implemented. Keep this file in sync with
`common_blender_utils.py` once naming helpers are written.
