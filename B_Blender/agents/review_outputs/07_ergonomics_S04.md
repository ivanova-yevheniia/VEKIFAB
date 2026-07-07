# 07 — Ergonomics Review — S04 Vision Inspection

- **Reviewer:** 07 Ergonomics Engineer · **Verdict:** PASS
- **Build after pass:** 138 objects · 0 errors (built with 08 at the design checkpoint)

## Reach / height table
| Device | Height | Tilt | Reach OK? |
|---|---|---|---|
| HMI screen | 1.25 m centre | −12° | yes (1.20–1.45 range) |
| E-stop | 1.10 m | faces +Y | yes (reachable from aisle) |
| Belt work surface | 0.585 m top | — | pass-through, no manual lift |

## Scores (owned: ergonomics)
| Category | Score | Note |
|---|---|---|
| ergonomics | 4 | HMI pose correct, e-stop reachable, standing zone defined |
| safety | 4 | operator zone marked + matted |

## Findings (question: "can a real person use this comfortably?")
- **F-1 [minor]** Operator standing zone undefined → added an `OperatorMat`
  (anti-fatigue) in the +Y zone, aligned with the safety `WorkZone` outline.
- HMI height/tilt already within range — no change (do not relocate; layout fixed).

## Changes applied
New component `ergonomics` (`OperatorMat`). Assembly op `op_211_ergonomics`.

## Handoff → 08 Industrial Designer
Function is legible; refine the visual family without adding decoration.
