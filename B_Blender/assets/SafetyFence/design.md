# Safety Fence — Design Specification

## Purpose
Guards hazardous zones (e.g. robot cells); defines keep-out perimeters.

## Geometry
Yellow posts, mesh infill panels and floor feet — one repeatable bay.

## Parameters
- `bay_width_m` (0.5-1.5) — Bay width.
- `height_m` (1.2-2.4) — Fence height.

## Materials
- `safety_yellow`
- `metal_light`
- `metal_dark`

## Hierarchy
```
FENCE_Post_* (boxes, collider)
  FENCE_Panel_* (panels, collider)
  FENCE_Foot_* (boxes)
```

## Connections
- `post_end` at post tops/sides, axis +/-X — bay-to-bay coupling
- `gate` at any bay, axis +Y — replace panel with interlocked gate

## Typical dimensions
1.0 m bay width x 2.0 m height (repeatable)

## Unity collider type
Box per post + Box per panel

## Physics
Static. Blocking colliders; interlocked gate optional.

## LOD importance
medium

## Performance budget
~1.2k tris per bay

## Industrial design notes
Signal-yellow posts, grey welded-mesh infill (approximated as a thin panel), bolt-down feet.

## Manufacturer inspiration
Generic machine guarding in the Axelent / Troax / Satech idiom.
