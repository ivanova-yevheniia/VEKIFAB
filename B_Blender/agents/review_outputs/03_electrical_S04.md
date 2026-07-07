# 03 — Electrical / Controls Review — S04 Vision Inspection

- **Reviewer:** 03 Electrical Engineer · **Verdict:** PASS_WITH_NOTES
- **Build after pass:** 101 objects · 0 errors · 0 warnings

## Scores (owned: electrical_realism)
| Category | Score | Note |
|---|---|---|
| electrical_realism | 4 | every device now cabled to the cabinet; disconnect present |
| industrial_realism | 4 | sensors + controller make the "vision" function legible |
| safety | 2 | e-stop orientation + markings still open (→06) |
| maintenance_access | 2 | LOTO/hatch open (→05) |
| (others unchanged) | 3–4 | |

## Findings (question: "where does this cable terminate?")
- **F-1 [major]** No mains isolation → added `MainSwitch` (+knob/lever) on the
  cabinet door, service side.
- **F-2 [major]** Camera/ring/HMI were unpowered → added `CableDuct` along the
  back edge with `CameraCable`, `RingCable`, `HMICable` and a `CabinetRiser` into
  the enclosure. Every cable terminates at the cabinet.
- **F-3 [major]** No trigger for the vision cycle → added through-beam
  `SensorEntry`/`SensorExit` photo-eyes (red windows) at the tunnel in/out feed.
- **F-4 [minor]** No imaging hardware presence → added a `VisionController` (PoE /
  vision PC) on the cabinet with a run indicator LED.

## Changes applied
New component `electrical` (main switch, duct, 3 cable runs + riser, 2 sensors,
vision controller). Assembly op `op_207_electrical`.

## Handoff → 04 Pneumatic
The reject **bin** exists but nothing ejects a failed part into it — a diverter
actuator with air prep and isolation is required.
