# Cardboard Box — Design Specification

## Purpose
Kit tray / finished-product carton; the movable unit load on the line.

## Geometry
A single beveled box with a kraft-brown finish.

## Parameters
- `length_m` (0.2-0.6) — Box length.
- `height_m` (0.15-0.5) — Box height.
- `mass_kg` (0.2-5.0) — Rigidbody mass.

## Materials
- `cardboard`

## Hierarchy
```
BOX_Body (box, collider, rigidbody)
```

## Connections
- `base` at (0,0,0), axis -Z — stacks / rides on conveyor

## Typical dimensions
400x300x300 mm (variable)

## Unity collider type
Box (dynamic)

## Physics
Dynamic rigidbody (~0.6 kg) so the avatar can pick it up.

## LOD importance
low

## Performance budget
~60 tris

## Industrial design notes
Kraft brown, subtle flap seam, optional shipping label decal. Cheapest asset — instance freely.

## Manufacturer inspiration
Generic RSC shipping carton.
