# Robot Gripper

Reusable industrial asset (robotics). Two-finger parallel gripper end-effector.

| Field | Value |
|-------|-------|
| Asset ID | `robot_gripper` |
| Version | 1.0.0 |
| Category | robotics |
| Tags | robot, gripper, end-effector, tool |
| Typical size | 0.15 m body, 0.17 m fingers |
| Unity collider | Box (static) |
| LOD importance | high |
| Performance budget | ~120 tris |

## Files
- design.md, parameters.json, assembly.json, builder.json, preview.png

## Usage
Instantiated by the robot cell assembler (`composer/robot_cell_assembler.py`) which chains RobotPedestal -> RobotBase -> RobotArm -> RobotGripper into one kinematic hierarchy.
