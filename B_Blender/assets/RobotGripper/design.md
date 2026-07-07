# Robot Gripper — Design Specification

## Purpose
Parallel two-finger gripper mounted on the robot tool flange; handles the product.

## Geometry
A palm block with two parallel fingers pointing down.

## Parameters
- see parameters.json (dimensions are the source of truth)

## Materials
- `white_panel`
- `metal_dark`

## Hierarchy
```
ROBOTGRIPPER_Palm
```

## Connections
- mount_socket at local origin (attaches to parent link)
- tool_socket at node `gripper` (attaches the next asset)

## Typical dimensions
0.15 m body, 0.17 m fingers

## Unity collider type
Box (static)

## Physics
Kinematic (tool0); grips the product.

## LOD importance
high

## Performance budget
~120 tris

## Industrial design notes
White body + dark fingers; simple, clean end-effector.

## Manufacturer inspiration
Generic 2-finger parallel gripper.
