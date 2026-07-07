# MF-IP-100 — Whole-Line Integration Review (no geometry changed)

Reviewed as ONE production system, not 7 stations. Verdict: **currently reads as seven
independent scenes.** Evidence below is measured from the 7 `*_parameters.json` specs.

## Hard evidence

### Production flow is not continuous
| | S01 | S02 | S03 | S04 | S05 | S06 | S07 |
|---|---|---|---|---|---|---|---|
| world X | 2.5 | 6.0 | 10.0 | 12.5 | 16.5 | 19.17 | 22.5 |
| world Y | 6.0 | 6.0 | 6.0 | 6.0 | 6.0 | **6.12** | **6.12** |
| conveyor belt top | 0.42 | **0.43 (plain block)** | **0.43 (plain block)** | **0.54** | 0.42 | 0.42 | 0.42 |
| rollers? | yes | **no** | **no** | yes | yes | yes | yes |

- **Line jogs sideways +0.12 m** at S05→S06 (Y 6.0→6.12). The centerline is not straight.
- **Irregular pitch**: ΔX = 3.5, 4.0, 2.5, 4.0, 2.67, 3.33 m — no bay module; inter-station
  gaps are random and unbridged.
- **Conveyor height steps**: S04 belt is **12 cm higher** than the rest; a carton would
  step up into vision and back down. Two conveyor *families*: S02/S03 are old plain blocks,
  the other five are roller conveyors.

### Visual language / equipment families drift
- **Emission values differ**: S04 uses `led_white`=4.0 & `screen_dark`=1.2; every other
  station uses 2.5 & 1.0. Under one Unity light, S04's LEDs/screens glow brighter.
- **Material libraries diverge**: S03 = 15 mats (adds fence/gate mesh, drops cardboard/
  wood_pallet/worktop_grey); S04 = 13 mats (same drops). Each station also **re-declares the
  whole palette**, so Unity imports 7 duplicate "metal_light" etc. — no single source of truth.
- **Bench family varies**: S01 legs asymmetric (−1.06/+0.46); others symmetric ±0.8/±0.85;
  worktop widths 1.6–1.9. Frame is 40×40 everywhere (good) but footprints don't match.

### Storytelling — the product does not survive the line (biggest flaw)
The "same" MF-IP-100 device is a different mesh at every station:
`S02 0.12×0.08×0.045` · `S04 0.10×0.075×0.11 (pump w/ handle+connector)` ·
`S05 0.10×0.075×0.10` · then a carton `S06 0.20×0.14×0.11` vs `S07 0.22×0.16×0.12`.
A visitor **cannot follow one object** from load → assemble → test → pack → store.
There is no canonical device mesh and no canonical finished-carton.

### Labels / signage inconsistent
- Flow arrows: `→ S02`, `→ S03`, then ASCII `-> S04`, **S04 has no flow arrow at all**,
  then `→ S06 / → WAREHOUSE / → SHIPPING`. Mixed glyphs + a missing link (S04→S05).
- Info-board titles: "Loading Station" / "Assisted Assembly" / "Robot Handling Cell" /
  "Vision Inspection" / "Functional Test" / "Packaging" / "Storage & Dispatch" — no common
  convention and **no S0x station ID** on the hero boards.

### Operator / maintenance / logistics / safety consistency
- Operator side is +Y everywhere (good). But e-stop heights differ (S01 0.98 vs 1.10),
  stack-light tops and info-board tops differ → ragged skyline.
- Service side mixed: cabinets on −X (S01/S05/S06) vs −Y (S03/S07). No single service aisle.
- HMI: S01 arm-mounted vs poles elsewhere; each HMI has bespoke text layout/sizes/colors —
  reads as 7 different control vendors, not one line controller.
- **No factory scene**: each station carries its own review floor + review light + its own
  info panel. There is no shared floor, one straight walkway with continuous edge striping,
  bridged conveyors, or a line-level andon/overview — so it literally is 7 scenes.
- Naming drift: composition `STATION_S06_*`/`STATION_S07_*` vs spec roots `STATION_06_*`.

## Prioritized improvements (do later)

### P0 — make it one continuous line (flow-breaking)
1. **Straighten the centerline**: set S06 & S07 world Y = 6.0 (remove the 0.12 m jog).
2. **One conveyor family + one belt height (0.42 m)**: rebuild S02 & S03 plain-block
   conveyors as roller conveyors; lower S04's conveyor from 0.54 to 0.42 (or add explicit
   transfer ramps). Same rollers, frame, side rails on all 7.
3. **Bridge the gaps / regularize pitch**: add continuous inter-station conveyor segments so
   output of N physically meets input of N+1 at the same Y and height (or set a common bay pitch).
4. **One canonical product**: define a single `MF-IP-100 device` mesh (fixed dims + look) and
   a single finished-carton mesh; reuse them identically at S02/S04/S05 (device) and S06/S07
   (carton) so one object is visibly tracked down the line.

### P1 — one visual/control system
5. **Single shared material library** with identical values (incl. emission): fix S04's
   led_white/screen_dark back to 2.5/1.0; give S03/S04 the full palette; treat one palette as
   the source of truth and dedupe materials on Unity import.
6. **Consistent flow labels**: all `→`, add the missing S04→S05 arrow, and put the `S0x`
   station ID on every info board and ID plate (one naming convention).
7. **One HMI template**: shared header bar + status line + metric rows, reused across stations
   (only the values change), and one HMI mounting style.

### P2 — factory context & storytelling
8. **Build a single factory scene** (`generate_full_factory` / unity_handoff): one continuous
   floor, one straight walkway aisle with consistent edge striping, line-wide keep-out only at
   S03, and a line-level overview/andon board.
9. **Align the skyline**: common e-stop height (1.10), stack-light top, and info-board top;
   consistent service side (−X cabinets) line-wide.
10. **Consistent bench family**: symmetric legs on a common footprint module (fix S01's
    asymmetric legs) so benches read as one catalogue product.

### P3 — polish / dedup
11. Resolve naming drift (`STATION_S0x` vs `STATION_0x`); material/mesh instancing across the
    line; unify info-title wording ("S0x · Name").

**Net:** P0 alone (straight centerline, one conveyor family/height, one product) converts
"7 scenes" into "one line." P1–P2 make it read as one designed factory.
