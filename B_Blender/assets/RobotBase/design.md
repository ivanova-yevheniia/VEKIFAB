# Robot Base — Design Specification

## Purpose
The fixed robot base carrying the J1 (waist) rotary flange.

## Geometry
A cylinder base with a lighter mounting flange on top.

## Parameters
- see parameters.json (dimensions are the source of truth)

## Materials
- `metal_dark`
- `metal_light`

## Hierarchy
```
ROBOTBASE_Body
```

## Connections
- mount_socket at local origin (attaches to parent link)
- tool_socket at node `base` (attaches the next asset)

## Typical dimensions
Ø 0.4 m, 0.16 m tall

## Unity collider type
Box (static)

## Physics
Static (link 0).

## LOD importance
medium

## Performance budget
~180 tris

## Industrial design notes
Machined dark casting + bright flange ring.

## Manufacturer inspiration
Generic robot base flange.
