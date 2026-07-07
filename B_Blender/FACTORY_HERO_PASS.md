# FACTORY_HERO_PASS — MF-IP-100 Line Integration (pre-Unity)

Chief-Factory-Engineer pass to make S01–S07 read as **one production line**, not seven
scenes. Spec-only (`*_parameters.json` / `*_assembly.json`); `procedural_builder` untouched;
Unity names, tags, triggers and animation placeholders preserved; layouts not redesigned.

## Validation (all 7 rebuilt)
| Station | Objects | Triangles (<20k) | Materials (≤16) | Build |
|---|---|---|---|---|
| S01 Loading | 285 | 17,428 | 16 | 0 err / 0 warn |
| S02 Assembly | 198 | 17,002 | 13 | 0 err / 0 warn |
| S03 Robot Cell | 174 | 16,252 | 15 | 0 err / 0 warn |
| S04 Vision | 260 | 17,064 | 13 | 0 err / 0 warn |
| S05 Functional Test | 206 | 17,711 | 14 | 0 err / 0 warn |
| S06 Packaging | 212 | 16,298 | 16 | 0 err / 0 warn |
| S07 Storage | 219 | 17,960 | 15 | 0 err / 0 warn |

Unity names/tags/placeholders verified intact on every changed station; 0 name collisions.

## Modifications performed

### P0.1 — ONE canonical product + ONE canonical carton
- Canonical **MF-IP-100 device** = `0.10 × 0.075 × 0.11`, `white_panel`, screen face.
  Applied so the same device is recognizable at **S02** (`PHYS_Assembly_Part_1..4`),
  **S04** (`PHYS_Vision_Product_1`, reference), **S05** (`PHYS_FunctionalTest_Box_1`).
- Canonical **finished carton** = `0.22 × 0.16 × 0.12` cardboard + label. Applied at
  **S06** (`PHYS_Packaging_Box_1/2/3`, inner liner) so the box S06 seals is the box S07
  stores (**S07** cartons were already `0.22×0.16×0.12`).

### P0.2 — ONE conveyor family
- **S02** and **S03** simplified block conveyors rebuilt as the **roller-conveyor family**
  already used by S04–S07 (belt plane + frame tie + side rails + 8 rollers + 4 legs + feet
  + output gearmotor). Belt names preserved (`CONVEYOR_Assembly_*`, `CONVEYOR_RobotCell_*`).
- Removed S03's now-redundant `conveyor_detail` (duplicate rollers) + its assembly op.

### P0.3 — Unified conveyor elevation (0.42 m belt top)
- S02/S03 rebuilt at belt-top **0.424** (family standard).
- **S04** inspection deck lowered as one coherent sub-assembly (bench + belt + tunnel +
  camera + ring + product + mounts) by **-0.14 m** so its belt top moved **0.56 → 0.42**;
  bench legs shortened 0.46 → 0.32 to keep the load path; floor peripherals (HMI, cabinet,
  stack, e-stop, reject bin) untouched. Internal camera/ring/product relationships preserved.
- Result: every station transports at **≈0.42 m** (0.42–0.424, ±4 mm).

### P0.4 — Straight production centerline
- **S06** and **S07** moved from world **Y 6.12 → 6.00** (station shifted −0.12 m, all
  absolute-positioned children shifted with it). All 7 stations now share centerline Y = 6.0.

### P1 — Common design language (measured inconsistencies fixed)
- **Emission values unified**: S04 `led_white` 4.0 → 2.5, `screen_dark` 1.2 → 1.0 (all 7
  now identical) so LEDs/screens glow the same under one Unity light.
- **Info-panel line aligned**: all boards/posts/titles/bodies/triggers to world Y
  8.60/8.62/8.64/9.30.
- **Flow labels**: glyph unified to `→` (fixed S03 ASCII `->`); added the missing
  **S04 `→ S05`** arrow; the chain now reads `→ S02 → S03 → S04 → S05 → S06 → WAREHOUSE
  → SHIPPING`.
- **Info titles** unified to `S0x · Name` convention across all 7.
- Already consistent from the hero passes (reused recipes): cabinet (glass door + DIN
  interior), HMI (bezel + screen + pole + live text), stack light (3 segments + dome),
  e-stop (yellow plate + red mushroom), roller-conveyor family, worktop/40×40 frame,
  operator +Y front, canonical 16-key palette values.

### P2 — Import-ready (no factory floor built, per instruction)
- Consistent **output direction** (+X flow) and **operator side** (+Y front) on all 7.
- Consistent **conveyor interface** (same family, same 0.42 m plane, same 0.52 m belt
  width) so inter-station segments meet cleanly.
- Consistent **floor-marker widths** (safety stripe 0.10 m; zones outlined).
- Stations authored at world coordinates on one straight centerline — drop each `.glb` in
  and they align.

### P3 — Digital-twin placeholders (all preserved, one added)
No placeholder removed. Coverage per motion the twin must show:
- product movement → conveyors kinematic + `PHYS_*` products; `PalletMoveAnimation` (S07)
- robot motion → S03 named kinematic chain (`PHYS_RobotCell_*`) + `Gripper`
- inspection → S04 `AIHeatmap/AILaser/AICrosshair/AIBBox`, sensors, andon
- functional test → S05 `ClampAnimation/ConnectorAnimation/ProbeAnimation/PressureGauge/
  TestStartButton/PassLamp/FailLamp/FixtureClosed/FixtureOpen`
- packaging → S06 `OpenBox/InsertProduct/CloseBox/PrintLabel/ApplyLabel/BarcodeScan/Reject`
- warehouse logistics → S07 `PalletMove/InventoryUpdate/BarcodeRead/RFIDRead/ShelfIndicator/
  DispatchReady/PalletLoaded`

## Before / After (line level)
| Aspect | Before (7 scenes) | After (1 line) |
|---|---|---|
| Centerline Y | S06/S07 jog to 6.12 | all 7 on 6.00 |
| Transport height | 0.42 / 0.43 / **0.56** mixed | all ≈ **0.42** |
| Conveyor family | S02/S03 plain blocks + 5 roller | **all 7 roller family** |
| Product identity | 4 different device meshes | **one canonical device** |
| Finished carton | S06 0.20×0.14 vs S07 0.22×0.16 | **one canonical carton** |
| Emission | S04 brighter (4.0/1.2) | **identical (2.5/1.0)** |
| Flow arrows | `→`, `->`, missing | **unbroken `→` chain** |
| Info titles | 7 styles | **`S0x · Name`** |

## Remaining recommendations — UNITY ONLY (not implemented here)
- **Materials**: dedupe the 7 per-station palettes into one shared library on import (map
  engine material names → one set); author final PBR/roughness/metallic in Unity.
- **Lighting**: single scene lighting rig (the review area lights are export-excluded).
- **Post-processing**: bloom/AO/color-grade in Unity.
- **Factory hall / floor**: build the room, continuous floor, aisle, walls in Unity; add
  short filler conveyor segments to physically bridge the (now height-aligned) station gaps.
- **Navigation / avatars**: walkthrough avatar + NavMesh in Unity.
- **Camera**: cinematic / walkthrough cameras in Unity.
- **Optional P1 polish (Blender, minor)**: harmonize e-stop mounting height (S01 0.98 →
  1.10) and S01's arm-HMI to the pole-HMI family; symmetric bench legs on S01. Non-blocking.

**Result:** on import, S01–S07 sit on one straight 0.42 m transport line, run the same
roller conveyor family, pass the same recognizable device and finished carton down the
line, glow identically, and label the flow as one unbroken chain — the MF-IP-100 reads as
one professionally engineered smart factory.
