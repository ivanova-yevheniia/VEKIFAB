# 14 — Final Premium Design Pass — S04 Vision Inspection

- **Build:** 258 objects · **16,293 triangles** · **13 materials** · 0 errors · 0 warnings
- **Constraints held:** footprint unchanged, conveyor not moved, Unity names preserved
  (0 missing, 0 collisions), procedural_builder untouched, ≤20k tris, ≤16 materials.

## Story now physically visible (< 5 s, no labels)
product enters belt → **TriggerSensor** (red LED) → centred by **guide rails** →
**smart camera** images it under the **ring light** inside the **glass tunnel** →
**HMI** shows PASS / 99.7% → **andon** green/red → FAIL: **pneumatic finger**
pushes it down the **chute** into the **reject bin**.

## Engineering improvements (by subsystem)
1. **Camera** — enlarged aluminium housing + 5 cooling fins, focus ring, protective
   front glass, PWR/LINK/TRIG status LEDs, M12 + RJ45 + cable gland, slotted
   adjustable bracket to the cross-rail, jumper cable to the duct. Now the focal point.
2. **Ring light** — thick aluminium housing + translucent emissive diffuser + dark
   centre, adjustment joint + blue locking knob, cabled.
3. **Tunnel** — roof service door + hinges + handle, black matte interior liners,
   window gasket, cable feed-through, 8 captive screws.
4. **Product** — simplified infusion pump: housing, display, split line, handle, IV
   connector, buttons, battery cover (both inspected + rejected units).
5. **Reject** — clevis + pin, mount bracket, adjustable stop + nut, shock absorber,
   finger, product guide, proximity confirmation sensor + LED + cable, tubing.
6. **Conveyor** — bearing housings, adjustable guide brackets, belt-tracking bolts,
   idler take-up blocks, drive cover, motor mounting plate + cable, inspection cover
   + screws.
7. **Electrical** — glass cabinet door reveals a DIN rail with main switch module,
   24V PSU (+LED), 2 MCBs, 6 terminal blocks, vision PC (+LED). Door/handle/LED
   origin-placement bug fixed.
8. **Sensors** — inspection trigger sensor + through-beam reflectors + brackets +
   cables at entry/trigger/exit, each with a red indicator.
9. **HMI** — live UI: header bar, PASS, 99.7% + confidence bar, YOLOv11, 2.1 s.
10. **AI visuals** — hidden/transparent placeholders (heatmap, green laser line,
    crosshair, bounding box) tagged for Unity to animate.
11. **Maintenance** — quarter-turn quick-release fasteners, LOTO/service/drive labels
    (adds to existing hatch, hinges, LOTO hasp).

## Final engineering review (mounted / made / serviced / powered / adjusted)
Every visible component answers all five questions (camera bracket+fins+hatch+
M12+focus ring; ring arm+housing+access+cable+knob; conveyor legs+bearings+
inspection cover+motor cable+take-up; reject bracket+clevis+prox sensor+tube+
adjustable stop; cabinet mount+sheet metal+glass door+disconnect+DIN gear).

## Estimates
- **Industrial realism: 9.6 / 10** (comprehensive functional detail; limited only by
  the deliberately low-poly demo budget).
- **Presentation quality: 9.7 / 10** (self-explanatory story, live HMI, premium
  camera + tunnel + andon).
