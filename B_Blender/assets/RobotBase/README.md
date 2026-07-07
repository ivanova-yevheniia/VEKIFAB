# Robot Base

Reusable industrial asset (robotics). Robot base casting with the J1 mounting flange.

| Field | Value |
|-------|-------|
| Asset ID | `robot_base` |
| Version | 1.0.0 |
| Category | robotics |
| Tags | robot, base, J1, structure |
| Typical size | Ø 0.4 m, 0.16 m tall |
| Unity collider | Box (static) |
| LOD importance | medium |
| Performance budget | ~180 tris |

## Files
- design.md, parameters.json, assembly.json, builder.json, preview.png

## Usage
Instantiated by the robot cell assembler (`composer/robot_cell_assembler.py`) which chains RobotPedestal -> RobotBase -> RobotArm -> RobotGripper into one kinematic hierarchy.
