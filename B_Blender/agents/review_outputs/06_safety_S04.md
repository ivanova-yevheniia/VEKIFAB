# 06 — Safety Review — S04 Vision Inspection

- **Reviewer:** 06 Safety Engineer (EN 60204-1 / ISO 12100 / ISO 13849) ·
  **Verdict:** PASS_WITH_NOTES
- **Build after pass:** 134 objects · 0 errors · 0 warnings

## Scores (owned: safety)
| Category | Score | Note |
|---|---|---|
| safety | 4 | e-stop corrected, guarded drive, markings, dual LOTO, hazard labels |
| presentation_quality | 4 | PASS/FAIL now dominant and self-explanatory |
| industrial_realism | 4 | reads as a real inspection gate |

## Findings (question: "can anyone be hurt, can all energy be isolated?")
- **F-1 [blocker→resolved]** `EStopButton` was placed at the station origin
  (floor centre) via an `offset_m [0,0,0]` overriding its parent offset, and faced
  −Y. Relocated onto the plate at [-0.55, 0.665, 1.10] facing the operator (+Y).
- **F-2 [major]** PASS/FAIL status not dominant → added an `Andon` beacon (big
  green PASS + red FAIL) on the tunnel exit facing the aisle, on a bracket.
- **F-3 [major]** Rotating gearmotor unguarded → added `DriveGuard` +
  `DriveGuardSide`.
- **F-4 [major]** No floor markings → added `SafetyStripe` (walkway edge),
  `WorkZone` (operator zone), `RejectZone` (bin drop).
- **F-5 [minor]** No hazard labels → added `VoltageSticker` (⚡ on cabinet) and
  `RejectSticker` (! at the auto-reject).

## Changes applied
New component `safety_systems` (13 nodes); edited `emergency_stop.button`.
Assembly op `op_210_safety_systems`.

## Handoff → 07 Ergonomics
E-stop is now reachable and correct; confirm operator standing zone and add an
anti-fatigue provision.
