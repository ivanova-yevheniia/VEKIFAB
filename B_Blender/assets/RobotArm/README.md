# Robot Arm

Reusable industrial asset (robotics). 6-axis articulated arm: waist-shoulder-upper arm-elbow-forearm-wrist.

| Field | Value |
|-------|-------|
| Asset ID | `robot_arm` |
| Version | 1.0.0 |
| Category | robotics |
| Tags | robot, arm, 6-axis, kinematic |
| Typical size | ~0.9 m reach |
| Unity collider | Box per link (static) |
| LOD importance | high |
| Performance budget | ~1.2k tris |

## Files
- design.md, parameters.json, assembly.json, builder.json, preview.png

## Usage
Instantiated by the robot cell assembler (`composer/robot_cell_assembler.py`) which chains RobotPedestal -> RobotBase -> RobotArm -> RobotGripper into one kinematic hierarchy.
