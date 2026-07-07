# 01 — Mechanical Review — S04 Vision Inspection

- **Reviewer:** 01 Mechanical Engineer · **Verdict:** PASS_WITH_NOTES
- **Build after pass:** 66 objects · 0 errors · 0 warnings

## Scores (0–5)
| Category | Score | Note |
|---|---|---|
| industrial_realism | 3 | supports read now, conveyor still slab (→02) |
| mechanical_integrity | 4 | all floats resolved; load paths explicit |
| manufacturability | 2 | conveyor/camera not yet producible (→02) |
| maintenance_access | 2 | no service hatch yet (→05) |
| safety | 2 | e-stop grounded but orientation/markings (→06) |
| ergonomics | 3 | unchanged |
| electrical_realism | 2 | no cabling yet (→03) |
| visual_consistency | 3 | unchanged |
| unity_readiness | 4 | names preserved, colliders intact |
| presentation_quality | 3 | improving |

## Findings (question: "where does the load go?")
- **F-1 [major]** Conveyor in/out sections cantilever ~0.4 m past the bench with
  no support → added 4 `ConvLeg_*` + `ConvFoot_*` at x±1.45.
- **F-2 [major]** Ring light floated at z1.0 on nothing → added 3 `RingArm_*`
  dropping from the tunnel roof to the ring.
- **F-3 [major]** Camera hung on a 50 mm stub → added a `CameraRail` cross-member
  between the tunnel posts + a `CameraBracket` (adjustable mount).
- **F-4 [major]** E-stop floated at z1.1 → added `EStopPost` + `EStopPostFoot`.
- **F-5 [minor]** HMI/stack-light poles lacked base plates → added `HMIFoot`,
  `StackLightFoot`.
- **F-6 [minor]** Rejected `PHYS_Vision_Product_2` hovered above the bin → rested
  it at z0.30 inside the bin.

## Changes applied
New component `mech_supports` (CameraRail, CameraBracket, RingArm_1..3,
ConvLeg_1..4, ConvFoot_1..4, EStopPost, EStopPostFoot, HMIFoot, StackLightFoot);
edited `product_2` rest height. Assembly op `op_200_mech_supports` added.

## Handoff → 02 Manufacturing
The conveyor is still a flat slab and the camera is a tiny box — both need to
become producible, catalogue-like modules. Camera cross-rail is in place to hang
a proper camera from.
