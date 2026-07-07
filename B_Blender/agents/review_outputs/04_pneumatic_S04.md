# 04 — Pneumatic Review — S04 Vision Inspection

- **Reviewer:** 04 Pneumatic Engineer · **Verdict:** PASS_WITH_NOTES
- **Build after pass:** 114 objects · 0 errors · 0 warnings

## Air circuit (one-line schematic)
`shop air → AirValve (manual isolation / LOTO) → FRL (filter+regulator+bowl) →
AirLine_1 → RejectValve (solenoid) → AirLine_2 → RejectPusher (cylinder) →
paddle ejects FAIL part → RejectChute → RejectBin`. Every hop exists in the model.

## Scores (owned: pneumatic realism → electrical_realism/safety)
| Category | Score | Note |
|---|---|---|
| electrical_realism | 4 | pneumatics complete + isolatable |
| industrial_realism | 4 | the reject action is now legible |
| safety | 3 | air LOTO added; markings/e-stop still →06 |
| maintenance_access | 3 | isolation valve reachable; hatch still →05 |

## Findings (question: "where does the air come from, and what does it do?")
- **F-1 [critical→resolved]** Reject **bin** existed with no reject **mechanism** →
  added `RejectPusher` air cylinder + `RejectPusherRod`/`Paddle` and a
  `RejectChute` guiding failed parts into the bin.
- **F-2 [major]** No air preparation/isolation → added `FRL` (+bowl/knob), a
  manual `AirValve` with a `AirValveLever` (LOTO), a `RejectValve` solenoid, and
  `AirLine_1/2` tubing.

## Changes applied
New component `pneumatic_reject` (13 nodes). Assembly op `op_208_pneumatic_reject`.

## Handoff → 05 Maintenance
The isolation valve and disconnect are LOTO points; confirm lockout access and add
a camera-service hatch on the tunnel.
