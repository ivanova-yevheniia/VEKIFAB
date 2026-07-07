# Robot Arm — Design Specification

## Purpose
The articulated arm links (J1..J5). Built as a true parent chain so it can be rigged/animated in Unity.

## Geometry
Nested link chain: waist (Z) -> shoulder (Y) -> upper arm -> elbow (Y) -> forearm -> wrist (Z).

## Parameters
- see parameters.json (dimensions are the source of truth)

## Materials
- `white_panel`
- `metal_dark`

## Hierarchy
```
ROBOTARM_Waist
```

## Connections
- mount_socket at local origin (attaches to parent link)
- tool_socket at node `wrist` (attaches the next asset)

## Typical dimensions
~0.9 m reach

## Unity collider type
Box per link (static)

## Physics
Kinematic chain (posed, not animated here).

## LOD importance
high

## Performance budget
~1.2k tris

## Industrial design notes
White composite links + dark machined joints; proper joint order and proportions; no brand copy.

## Manufacturer inspiration
Generic 6-axis cobot (ABB/KUKA/FANUC/UR language, nothing copied).
## Robot metadata
- payload_kg: 3.0
- reach_m: 0.9
- repeatability_mm: 0.02
- axes: 6
- home_pose: {'waist_deg': 0, 'shoulder_deg': 90, 'elbow_deg': 90, 'tool_down': True}
