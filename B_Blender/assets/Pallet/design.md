# Pallet — Design Specification

## Purpose
Bulk load carrier for incoming material and finished goods.

## Geometry
A deck of boards over nine support blocks.

## Parameters
- `length_m` (0.8-1.2) — Pallet length.
- `width_m` (0.6-1.0) — Pallet width.

## Materials
- `wood_pallet`

## Hierarchy
```
PALLET_Deck (box, collider)
  PALLET_Board_* (boards)
  PALLET_Block_* (blocks)
```

## Connections
- `floor` at (0,0,0), axis -Z — floor / fork entry
- `top` at (0,0,deck), axis +Z — load surface

## Typical dimensions
1200x800x144 mm (EUR-class)

## Unity collider type
Box (static)

## Physics
Static by default; dynamic rigidbody option (~25 kg) for handling.

## LOD importance
low

## Performance budget
~400 tris

## Industrial design notes
Pale worn timber, chamfered board edges, visible fork openings between blocks.

## Manufacturer inspiration
Generic EUR/EPAL-proportion wooden block pallet.
