# S04 Vision Inspection Station — Industrial Design Specification

**Station ID:** S04 · **Type:** `vision_inspection_station`
**Governed by:** `design_specs/factory_style_guide.md` (this station must comply).
**Pipeline:** `requirements → parametric_specs → asset library → procedural_builder`.
Rendered from `parametric_specs/vision_inspection_parameters.json` +
`vision_inspection_assembly.json`. **Individual station prefab only — no full scene.**
**Units:** metres, Z-up → Unity Y-up. World position `[12.5, 6.0, 0.0]`, envelope
2.4 × 2.2 × 2.6 m (taller for the camera/tunnel), front = +Y, flow = +X.

## 1. Purpose
Automated optical quality gate: cameras check assembly correctness and label
quality on closed pumps arriving from the robot cell (S03), diverting failures
before functional test (S05).

## 2. Design intent
An **enclosed inspection tunnel** with a glass viewing window on the walkway side,
a downward AI camera and a bright LED ring for controlled, repeatable imaging —
in the factory palette (dark hood, aluminium posts, blue/screen accents), no brand
copy. Objective machine vision replaces manual inspection variance.

## 3. Elements
| Element | Objects | Notes |
|---------|---------|-------|
| Bench + frame | `COLLIDER_Vision_Base`, `STATION_04_VisionInspection_Leg_*`, `_Foot_*` | aluminium frame on levelling feet |
| Conveyor | `CONVEYOR_Vision_Input`, `CONVEYOR_Vision_Belt`, `CONVEYOR_Vision_Output` | product passes through the tunnel, +X |
| Inspection tunnel | `STATION_04_VisionInspection_Tunnel*` (top, side, **glass window**, 4 posts) | enclosed hood; window faces +Y walkway |
| AI camera | `CAMERA_AI_Inspection` (+ mount, lens, LED) | above the product, looking down |
| LED ring light | `STATION_04_VisionInspection_RingLight` | emissive ring under the camera |
| Product mockups | `PHYS_Vision_Product_1` (on belt, under camera), `PHYS_Vision_Product_2` (in reject bin) | inspected units |
| Reject bin | `STATION_04_VisionInspection_RejectBin` | diverted failures (−Y side) |
| HMI (state) | `STATION_04_VisionInspection_HMI` + `_HMIState` ("PASS") | shows the inspection result |
| Stack light | `STATION_04_VisionInspection_Stack*` | red/amber/green status |
| Emergency stop | `STATION_04_VisionInspection_EStop` | operator-reachable, +Y |
| Control cabinet | `STATION_04_VisionInspection_Cabinet` (+door, handle, LED) | electrical box, maintenance −Y |
| Info panel | `INFO_Vision_Panel` (+title, body) | faces +Y walkway |
| Trigger | `TRIGGER_Info_Vision` | Unity info event |

## 4. Materials
Canonical palette only, plus a semi-transparent `glass_window` for the viewing
side of the tunnel. Emissive: `screen_dark` (HMI), `led_white` (ring), stack-light
LEDs, cabinet/camera indicators.

## 5. Automation & safety
Fully automated inspection (~20 s, non-bottleneck); enclosed optics, so guarding is
the hood — no fence. E-stop + stack light + info panel per the style guide. Reject
diversion is automatic.

## 6. Material flow
Input from S03 (`CONVEYOR_Vision_Input`) → tunnel inspection → pass to S05
(`CONVEYOR_Vision_Output`); failures diverted to the reject bin.

## 7. Unity handoff
Naming: `STATION_04_VisionInspection_*`, `CONVEYOR_Vision_*`, `CAMERA_AI_Inspection`,
`PHYS_Vision_Product_*`, `COLLIDER_Vision_*`, `TRIGGER_Info_Vision`, `INFO_Vision_Panel`.
Colliders/rigidbodies/triggers/tags exported as glTF `extras`; prefab
`vision_inspection.glb` (Y-up).

## 8. Performance
Measured **9,885 triangles** (target < 20 k), **49 objects**, 13 shared materials
(≤16 rule), low cylinder segment counts, instanced legs/feet/posts/stack segments.
