# Robot Pedestal

Reusable industrial asset (robotics). Bolted floor pedestal that mounts the robot base.

| Field | Value |
|-------|-------|
| Asset ID | `robot_pedestal` |
| Version | 1.0.0 |
| Category | robotics |
| Tags | robot, pedestal, mount, structure |
| Typical size | 0.5 x 0.5 x 0.5 m |
| Unity collider | Box (static) |
| LOD importance | medium |
| Performance budget | ~40 tris |

## Files
- design.md, parameters.json, assembly.json, builder.json, preview.png

## Usage
Instantiated by the robot cell assembler (`composer/robot_cell_assembler.py`) which chains RobotPedestal -> RobotBase -> RobotArm -> RobotGripper into one kinematic hierarchy.
