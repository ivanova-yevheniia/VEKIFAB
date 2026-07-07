# 05 — Maintenance Review — S04 Vision Inspection

- **Reviewer:** 05 Maintenance Engineer · **Verdict:** PASS_WITH_NOTES
- **Build after pass:** 121 objects · 0 errors · 0 warnings

## Serviceability matrix
| Module | Access route | Isolation | Fastener side |
|---|---|---|---|
| Camera / lens | new `ServiceHatch` (hinged, −Y) | MainSwitch (LOTO hasp) | service (−Y) |
| Ring light | via hatch / open front window | MainSwitch | −Y |
| Reject actuator | `AirValve` lever (LOTO) | pneumatic isolation | +Y/output |
| Cabinet | hinged door + handle | MainSwitch on door | −Y |
| Belt / rollers | open frame, guides removable | MainSwitch | side |

## Scores (owned: maintenance_access)
| Category | Score | Note |
|---|---|---|
| maintenance_access | 4 | camera hatch + dual LOTO + reachable valves |
| industrial_realism | 4 | window frame reads as a real inspection viewport |
| safety | 3 | LOTO hasp added; e-stop/markings still →06 |

## Findings (question: "what breaks after five years, and can it be reached?")
- **F-1 [major]** Camera/optics unreachable inside a closed shroud → added a
  hinged `ServiceHatch` (+ `HatchHinge_1/2`, `HatchHandle`) on the service side.
- **F-2 [minor]** Front glass read as a floating pane → added `WindowFrameTop/
  Bottom` so it is a framed inspection viewport.
- **F-3 [minor]** No visible lockout on the disconnect → added `LotoHasp`.

## Changes applied
New component `service_access` (6 nodes). Assembly op `op_209_service_access`.

## Handoff → 06 Safety
E-stop button is mislocated (sits at origin, not on the plate) and faces the wrong
way; no floor markings, guards or dominant PASS/FAIL indicator yet.
