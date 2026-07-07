# Cable Chain — Design Specification

## Purpose
Routes and protects cables and air lines to moving axes and along frames.

## Geometry
A row of identical short links approximating an articulated chain.

## Parameters
- `length_m` (0.2-3.0) — Chain run length.
- `link_count` (4-60) — Number of links.

## Materials
- `rubber_black`

## Hierarchy
```
CHAIN_Link_* (boxes)
```

## Connections
- `fixed_end` at (-L/2,0,z), axis -X — anchor to frame
- `moving_end` at (+L/2,0,z), axis +X — anchor to moving carriage

## Typical dimensions
0.5 m run, ~50 mm link pitch

## Unity collider type
None (visual)

## Physics
Static visual (kinematic if animated); no collider by default.

## LOD importance
low

## Performance budget
~300 tris

## Industrial design notes
Matte black polymer links, visible pin joints; keep segment count modest.

## Manufacturer inspiration
Generic energy chain in the igus e-chain / Kabelschlepp idiom.
