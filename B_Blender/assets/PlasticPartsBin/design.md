# Plastic Parts Bin — Design Specification

## Purpose
Presents small components for manual picking at assembly and kitting stations.

## Geometry
An open-topped tapered box with a front lip, tilted toward the operator.

## Parameters
- `width_m` (0.1-0.5) — Bin width.
- `tilt_deg` (-20 to 0) — Forward tilt.

## Materials
- `blue_accent`

## Hierarchy
```
BIN_Body (box, collider)
  BIN_Lip (box)
```

## Connections
- `shelf` at (0,0,0), axis -Z — sits on shelf/rail

## Typical dimensions
300x400x200 mm (size 4 class)

## Unity collider type
Box (static)

## Physics
Static by default; optional dynamic rigidbody for handling demos.

## LOD importance
low

## Performance budget
~200 tris

## Industrial design notes
Semi-gloss coloured polymer, label card slot on the front lip, stackable profile.

## Manufacturer inspiration
Generic parts bin in the SSI Schaefer / Bito idiom.
