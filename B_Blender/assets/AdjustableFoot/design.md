# Adjustable Foot — Design Specification

## Purpose
Levels a frame on an uneven floor and damps vibration; terminates every leg of a bench, cabinet or cell.

## Geometry
A rubber base disc, a threaded stud, and a hex adjustment nut. Two short cylinders plus a low-poly hex nut.

## Parameters
- `height_m` (0.04-0.12) — Overall foot height.
- `base_radius_m` (0.02-0.05) — Rubber base radius.

## Materials
- `rubber_black`
- `metal_light`
- `metal_dark`

## Hierarchy
```
FOOT_Base (cylinder, collider)
  FOOT_Stud (cylinder)
  FOOT_Nut (hex cylinder)
```

## Connections
- `mount` at (0,0,top), axis +Z — threads into profile/leg end

## Typical dimensions
Ø 60 mm base, M12 stud, 40-120 mm height

## Unity collider type
Box (static)

## Physics
Static. No rigidbody.

## LOD importance
low (small, seen at floor level)

## Performance budget
~120 tris

## Industrial design notes
Zinc/stainless stud, black rubber pad, hex adjuster. Subtle detail that signals real machine mounting.

## Manufacturer inspiration
Generic levelling foot in the item / Bosch Rexroth accessory idiom.
