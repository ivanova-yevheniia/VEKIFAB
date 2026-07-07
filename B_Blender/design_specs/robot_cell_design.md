# S03 Robot Handling Cell — Industrial Design Specification

**Station ID:** S03 · **Type:** `robot_handling_cell` · **Role:** Hero station —
the visual centrepiece of the Unity walkthrough.
**Governed by:** `design_specs/factory_style_guide.md` (this station must comply).
**Pipeline:** `requirements → parametric_specs → industrial asset library →
procedural_builder`. Rendered from `parametric_specs/robot_cell_parameters.json`
+ `robot_cell_assembly.json`. **No pipeline bypass.**
**Units:** metres, Blender Z-up → Unity Y-up. World position `[10.0, 6.0, 0.0]`,
envelope 3.0 × 3.0 × 2.5 m, front = +Y (walkway), flow = +X.

---

## 1. Purpose
A modern, collaborative-style robot handling cell. A fenced 6-axis arm receives
assembled pumps from S02 on the input conveyor, closes/reorients them and places
them onto the output conveyor to S04. It is the most dynamic and recognisable
station on the line — designed to read instantly as "smart automation".

## 2. Design intent (generic — nothing copied)
A clean industrial arm in the **factory style palette**: white composite links,
dark machined joints, subtle blue accents — the modern cobot register of ABB /
KUKA / FANUC / Universal Robots **without reproducing any of them**. No brand
orange, no specific product geometry. Guarding, signalling and controls follow
the same catalogue-module language as every other station.

## 3. The robot (believable, not kinematically exact)
A clean articulated arm with correct **proportions and joint order** — posed, not
simulated:

| Link | Primitive | Material | Notes |
|------|-----------|----------|-------|
| Pedestal / base plinth | box | `metal_dark` | `COLLIDER_RobotCell_Pedestal`, bolted to floor |
| Base | cylinder | `metal_dark` | mounting flange |
| Waist | cylinder (Z) | `white_panel` | J1 rotator column |
| Shoulder | cylinder (Y) | `metal_dark` | J2 pivot |
| Upper arm | box | `white_panel` | rises vertically |
| Elbow | cylinder (Y) | `metal_dark` | J3 pivot |
| Forearm | box | `white_panel` | reaches horizontally (+X) |
| Wrist | cylinder (Z) | `metal_dark` | J4/J5 |
| Gripper | box + 2 fingers | `white_panel` / `metal_dark` | 2-finger parallel gripper |

**Home pose:** waist centred, upper arm vertical, forearm extended along **+X**
toward the place point, gripper facing down — a clear, readable "reach" silhouette
from the walkway.

## 4. Robot reference points & zones
Exposed as tagged markers / volumes for Unity (not decorative):

- **Pick point** — `PHYS_RobotCell_PickPoint` (blue), local `(-0.75, 0.0, 0.5)`,
  above the input transfer.
- **Place point** — `PHYS_RobotCell_PlacePoint` (green), local `(0.58, -0.2, 0.6)`,
  under the gripper toward the output transfer.
- **Home pose** — the posed configuration above (documented; the arm is built in it).
- **Working envelope** — `TRIGGER_RobotCell_WorkEnvelope`, a wire volume
  (~2.2 × 2.0 × 1.7 m) enclosing the arm's reach; hidden in render, exported as a
  Unity trigger.
- **Operator safe zone** — `STATION_03_RobotCell_OperatorZone`, a yellow floor
  marking outside the gate on the +Y (walkway) side.
- **Robot restricted zone** — `STATION_03_RobotCell_RestrictedZone_*`, a yellow
  hazard floor outline inside the fence around the arm.

## 5. Safety fencing & access gate
- Perimeter guard: **signal-yellow posts** on bolt-down feet + **grey welded-mesh
  infill** (semi-transparent `fence_mesh` panels, ~1.8 m) on a ~2.7 m square within
  the envelope.
- **One access gate** on the **+Y** (operator/walkway) side — a semi-transparent
  blue framed gate (`gate_mesh`), shown swung open, with a green interlock
  indicator (`STATION_03_RobotCell_GateInterlock`).
- Conveyor pass-throughs on the ±X sides (mesh gaps at the belt line).

## 6. Controls, electrical & signalling
- **Emergency stop** on the gate post, operator-reachable (`led_red` on
  `safety_yellow`).
- **Stack light** (red/amber/green) on the front-right corner post (~2.3 m).
- **HMI** on a pole on the operator side, tilted −12°, emissive glass.
- **Electrical cabinet** behind the back fence (maintenance side, −Y): door,
  handle, green power LED.
- **Cable routing**: a black e-chain (`cable_chain`) runs from the cabinet to the
  robot base — no free-hanging cables.

## 7. Lighting & markings
- **Overhead task light** bar (emissive `led_white`) over the cell; a review-only
  area light (excluded from glTF).
- **Yellow floor markings**: restricted-zone outline inside; operator safe-zone
  outside the gate.

## 8. Warning labels (ASCII, style typography)
- `WARNING - ROBOT CELL - KEEP CLEAR` on the front-right panel.
- `S03 - ROBOT CELL` ID plate on the front-left panel.
- `-> S04` flow arrow by the output conveyor.

## 9. Material flow
Input conveyor (`CONVEYOR_RobotCell_Input`, from S02/C02) on −X → robot →
output conveyor (`CONVEYOR_RobotCell_Output`, to S04/C03) on +X.

## 10. Maintenance access
Cabinet on the −Y service side with door clearance; the +Y gate gives operator
access into the cell; fence feet are bolt-down and posts are on a module grid.

## 11. Naming & Unity handoff
Follows the WP B conventions: `STATION_03_RobotCell_*`, `PHYS_RobotCell_*`,
`COLLIDER_RobotCell_*`, `CONVEYOR_RobotCell_*`, `INFO_RobotCell_Panel`,
`TRIGGER_Info_RobotCell` / `TRIGGER_RobotCell_WorkEnvelope`. Colliders/rigidbodies/
triggers/tags exported as glTF `extras`.

## 12. Performance
Measured **12,084 triangles** for the whole cell (target < 25,000). Low segment
counts (cylinders 14–20), shared materials (12, ≤16 rule), instanced fence
posts/panels/feet and cable links. Unity-ready glb, Y-up.

## 13–18 (per style guide)
Structural, material, colour, LOD, surface-finish, and Blender-modelling
conventions all inherit from `factory_style_guide.md`; this station adds only the
robot arm and the fenced-cell composition. Where this document and the style guide
differ, **the style guide wins**.
