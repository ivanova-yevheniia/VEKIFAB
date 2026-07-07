# Roller Conveyor — Design Specification

## Purpose
Transports trays, cartons and fixtures between stations along the line.

## Geometry
Two side frame rails, a row of rollers on the Y axis, and four support legs.

## Parameters
- `length_m` (0.5-3.0) — Conveyor length.
- `width_m` (0.3-0.8) — Roller width.
- `belt_height_m` (0.3-0.9) — Roller top height.
- `roller_count` (4-24) — Number of rollers.

## Materials
- `metal_dark`
- `metal_light`

## Hierarchy
```
CONV_Frame (box, collider)
  CONV_RailFar (box)
  CONV_Roller_* (cylinders)
  CONV_Leg_* (boxes)
```

## Connections
- `in` at (-L/2,0,belt), axis -X — upstream transfer
- `out` at (+L/2,0,belt), axis +X — downstream transfer

## Typical dimensions
0.5-3.0 m length, 0.5 m width, belt top 0.45 m

## Unity collider type
Box (static frame) + Box (belt plane)

## Physics
Static frame. Rollers kinematic (spin only, visual). Product rides on top.

## LOD importance
medium (repeated along the line)

## Performance budget
~1.5k tris

## Industrial design notes
Powder-coated frame, bright rollers, drive-end motor block hint. Flow arrow decal.

## Manufacturer inspiration
Generic roller conveyor in the Interroll / Bosch Rexroth / Dorner idiom.
