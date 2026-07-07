# 00 — Engineering Plan — S04 Vision Inspection

- **Reviewer:** 00 Chief Engineer
- **Station:** S04 `STATION_04_VisionInspection` @ world [12.5, 6.0, 0]
- **Baseline build:** 49 objects · 9,885 tris · 0 errors · 13 materials
- **Requirement summary:** Inline machine-vision gate on the MF-IP-100 line —
  cameras check assembly/labelling, failed units are diverted automatically to a
  reject bin; PASS/FAIL status must be visible to the line.

## Objectives ("done" for S04)
Raise from prototype to industrial-demo quality **without changing the layout**,
staying ≤20k tris / ≤16 materials, preserving all Unity names. Function must be
legible without reading a label: *product enters → is imaged under light in a
shrouded tunnel → PASS continues / FAIL is ejected to the bin.*

## Risk map (by discipline)
| Risk | Owner |
|------|-------|
| Cantilevered conveyor ends + floating e-stop / ring light | 01 Mechanical |
| Flat-slab conveyor (no frame/rollers/guides/motor/sensors) | 02 Manufacturing |
| No cabling; camera/lights/sensors unpowered | 03 Electrical |
| Reject **bin** exists but no reject **mechanism** | 04 Pneumatic |
| No camera service access / inspection hatch | 05 Maintenance |
| No floor markings; e-stop faces wrong way; PASS/FAIL not dominant | 06 Safety |
| Operator zone undefined | 07 Ergonomics |
| Camera not visually dominant; accent discipline | 08 Industrial Designer |

## Assignments (focus areas)
- **01** de-float everything, add conveyor end legs, camera cross-rail + bracket,
  ring-light mounts, e-stop pedestal, pole feet.
- **02** rebuild conveyor as a real belt (side frames, rollers, product guide
  rails, drive motor); enlarge camera into a dominant machine-vision body; frame
  gussets + post end caps.
- **03** main disconnect, cable ducts + routed cables (camera, ring, HMI,
  sensors, reject valve) → cabinet; vision-controller hint.
- **04** pneumatic reject **pusher** at the outfeed firing FAIL parts into the
  bin; FRL + isolation valve + tubing.
- **05** hinged camera-service hatch on the tunnel; LOTO on disconnect + air.
- **06** correct e-stop orientation, conveyor pinch guards, floor markings,
  hazard/voltage stickers, and a dominant **PASS/FAIL andon beacon** at the exit.
- **07** anti-fatigue mat + work-zone outline; confirm HMI reach.
- **08** enforce palette/60-30-10, accent trims that reinforce the camera as hero.

## Acceptance bar
`mechanical_integrity`, `electrical_realism`, `safety`, `industrial_realism`,
`presentation_quality`, `customer_trust` must reach ≥3 (target ≥4). No floating
part. Reject mechanism present. PASS/FAIL readable at aisle distance. Build 0
errors, ≤20k tris, ≤16 materials, all Unity names preserved.

## Handoff → 01 Mechanical
Start with load paths: nothing may float, and the conveyor overhangs the bench by
0.4 m each end with no support — support it first.
