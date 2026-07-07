# Robot Pedestal — Design Specification

## Purpose
Rigid floor plinth that raises and mounts the robot base; bolts to the cell floor.

## Geometry
A single beveled box plinth.

## Parameters
- see parameters.json (dimensions are the source of truth)

## Materials
- `metal_dark`

## Hierarchy
```
ROBOTPEDESTAL_Body
```

## Connections
- mount_socket at local origin (attaches to parent link)
- tool_socket at node `pedestal` (attaches the next asset)

## Typical dimensions
0.5 x 0.5 x 0.5 m

## Unity collider type
Box (static)

## Physics
Static, non-movable.

## LOD importance
medium

## Performance budget
~40 tris

## Industrial design notes
Powder-coat charcoal, chamfered edges, floor-bolt pattern implied.

## Manufacturer inspiration
Generic robot pedestal (Rexroth/ABB floor-mount idiom).
