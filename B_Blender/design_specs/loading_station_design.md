# Loading Station — Industrial Design Specification

**Station ID:** S01
**Station type:** `loading_station`
**Line:** MF-IP-100 Infusion Pump Line
**Document role:** Design specification only. This document contains **no Blender
geometry and no Python code**. It is the design brief that a Blender generator
(WP B) consumes to build station S01.
**Units:** metres (SI), Blender Z-up; exported Y-up for Unity.
**Design language reference:** the modern industrial-automation aesthetic
common to Bosch Rexroth, Festo, ABB, Siemens and Beckhoff. All references below
describe a **generic** station in that visual language — no existing product is
reproduced.

---

## 1. Purpose

The Loading Station is the **head of the line**. It receives incoming bulk
components (pump housings, PCBAs, batteries, tubing sets) and stages them as
kitted trays that are released, one kit per cycle, onto the first conveyor
toward the Assisted Assembly Station (S02).

Design intent: communicate, at a glance and from the avatar walkway, that this
is where material *enters* the factory — a clean, well-lit, ergonomic infeed
point that looks organised, calm and manually operated but automation-ready.

Target visual read: *"a tidy, modern kitting bench with an aluminium-profile
frame, an ESD-safe worktop, angled part bins, a small HMI, and a powered roller
outfeed."*

---

## 2. Functional description

Material flow (left → right, +X):

1. Bulk components arrive on pallets in a floor-marked **pallet zone**.
2. An operator lifts components onto the **loading/kitting table**.
3. Components are placed into **kit trays** using **angled bin** picking.
4. The completed tray is pushed onto the **powered roller outfeed conveyor**.
5. The conveyor carries the tray to S02.

Cycle role: ~60 s per kit, buffered so downstream assembly is never starved.
The station is **semi-automated**: manual kitting, powered outfeed, HMI for
line status and kit confirmation, with an e-stop tied to the cell safety chain.

---

## 3. Industrial appearance

- **Overall impression:** modern, rectilinear, "clean-room adjacent". Light
  neutral surfaces with restrained blue accents and yellow only where safety
  demands it.
- **Frame:** built from **anodised aluminium extrusion profile** (40 × 40 mm and
  45 × 45 mm slot-profile look), the Bosch Rexroth / Festo structural-framing
  idiom — visible T-slots, black plastic slot covers, cast corner brackets.
- **Panels:** powder-coated sheet-metal infill panels and a laminated worktop.
- **Accents:** a single brand-accent colour (signal blue) on trims, bin fronts
  and the HMI bezel — the Siemens/Festo blue-grey register, not saturated.
- **Cable & air management:** cable trunking and a festooned energy chain along
  one upright; a small pneumatic FRL (filter-regulator-lubricator) cluster,
  Festo-style, mounted at knee height.
- **Cleanliness:** no exposed fasteners on show faces; edges chamfered; feet
  levelling-adjustable. Everything reads deliberate and maintainable.

---

## 4. Structural design

- **Base frame:** a rigid rectangular aluminium-profile table frame, ~0.9 m work
  height, on four adjustable levelling feet with anti-vibration pads.
- **Worktop:** a single ESD laminate top with a 15–20 mm apron, slight front
  overhang for clamping.
- **Back uprights:** two vertical profiles rising ~0.7 m above the worktop,
  carrying a **back rail** for the bin shelf, the tool/label holder and the HMI
  arm.
- **Bin shelf:** an angled shelf on the back rail, tilted ~15–20° toward the
  operator so bins present their open faces.
- **Outfeed conveyor:** a short powered roller/belt section cantilevered from the
  right end of the frame at belt-top height 0.40 m, aligned to the line centre
  (y = 6.0 m), feeding S02.
- **Enclosure logic:** open bench (no full guarding); the only guarded element is
  the conveyor pinch area, protected by a light fixed side guard.
- **Load path:** vertical loads → worktop → frame → feet → floor. The design
  should visually imply stiffness (corner gussets, cross-member under the top).

---

## 5. Main components

| # | Component | Function | Naming (WP B) |
|---|-----------|----------|---------------|
| 1 | Loading/kitting table (frame + worktop) | Primary work surface | `COLLIDER_Loading_Table`, `STATION_01_Loading_TableLeg_*` |
| 2 | Back uprights + back rail | Carry shelf/HMI/labels | `STATION_01_Loading_Upright_*` |
| 3 | Angled parts bins (4–6) | Present components for kitting | `STATION_01_Loading_Bin_*` |
| 4 | Kit trays / boxes (6–10) | Hold a kit of parts | `PHYS_Loading_Box_*` |
| 5 | Pallet zone marking | Marks pallet drop area | `STATION_01_Loading_PalletZone` |
| 6 | Pallets (2) | Bulk material carriers | `STATION_01_Loading_Pallet_*` |
| 7 | Powered outfeed conveyor | Releases kits to S02 | `CONVEYOR_Loading_Output` |
| 8 | Control panel / small HMI | Line status + kit confirm | `STATION_01_Loading_ControlPanel` |
| 9 | Emergency stop | Safety chain | `STATION_01_Loading_EStop` |
| 10 | Signal beacon (stack light) | Station status | `STATION_01_Loading_StackLight` |
| 11 | Task light bar | Illuminate worktop | `STATION_01_Loading_TaskLight` |
| 12 | Safety floor markings | Walkway/keep-out edges | `STATION_01_Loading_SafetyStripe` |
| 13 | Info panel | Avatar walkthrough text | `INFO_Loading_Panel` |
| 14 | Info trigger zone | Fires walkthrough info | `TRIGGER_Info_Loading` |
| 15 | Pneumatic FRL + cable chain | Services (visual detail) | `STATION_01_Loading_Services` |

---

## 6. Materials

Describe materials by their **physical read** so the generator can map them to
the `common_blender_utils` palette and PBR values.

| Material | Where used | Look | Suggested PBR |
|----------|-----------|------|---------------|
| Anodised aluminium profile | Frame, uprights, conveyor rails | Matte brushed light metal | `metal_light`: base 0.70/0.72/0.75, metallic 0.9, roughness 0.30–0.40 |
| Powder-coated steel (dark) | Feet, brackets, cabinet, conveyor frame | Fine-texture matte charcoal | `metal_dark`: 0.15/0.15/0.17, metallic 0.9, roughness 0.40 |
| ESD laminate worktop | Table top | Low-sheen mid-grey, slight texture | `white_panel`/custom grey, metallic 0.0, roughness 0.55 |
| Signal-blue polymer | Bin fronts, HMI bezel, trim | Semi-gloss blue | `blue_accent`: 0.10/0.35/0.75, roughness 0.40 |
| Safety yellow | Floor markings, e-stop backing | Matte hazard yellow | `safety_yellow`: 0.95/0.80/0.05, roughness 0.60 |
| Warning black | Label text, hazard stripes | Deep matte black | `warning_black`: 0.03³, roughness 0.70 |
| ABS / rubber | Slot covers, feet pads, roller lagging | Dark matte, slightly soft | `rubber_black`: 0.05³, roughness 0.90 |
| Cardboard (kraft) | Kit trays/boxes | Warm brown matte | custom `MAT_Cardboard`: 0.58/0.42/0.26, roughness 0.85 |
| Wood | Pallets | Pale worn timber | custom `MAT_WoodPallet`: 0.55/0.40/0.24, roughness 0.75 |
| Emissive screen | HMI display | Cool self-lit dark glass | `screen_dark` + emission ~1.0 |
| Emissive indicator | Stack-light segments | Red/amber/green glow | `red_emergency`, amber, `green_light`, emission 2–3 |

Keep the palette **restrained**: metals + one accent + safety colours. Avoid
rainbow surfaces; realism comes from value/roughness contrast, not hue.

---

## 7. Color palette

| Role | Colour | Hex (approx) | Notes |
|------|--------|--------------|-------|
| Primary structure | Light aluminium grey | `#B4B7BF` | 70–75% value, matte |
| Secondary structure | Charcoal | `#26262B` | feet, brackets, frames |
| Worktop | Neutral mid-grey | `#D9DBDE` | ESD look |
| Accent | Signal blue | `#1A59BF` | ≤15% of surface area |
| Safety | Hazard yellow | `#F2CC0D` | floor + e-stop only |
| Hazard contrast | Black | `#080808` | stripes, text |
| Status – ok | Green | `#0DCC33` | stack light |
| Status – warn | Amber | `#F2A20D` | stack light |
| Status – fault | Red | `#CC0D0D` | stack light / e-stop |
| Info panel | White board / black text | `#E8E8EA` / `#111` | walkway signage |

Rule of thumb (industrial designer's 60/30/10): **~60%** neutral metal, **~30%**
darker structure + worktop, **~10%** accent, with safety colours *outside* that
budget because they are functional, not decorative.

---

## 8. Dimensions

Master footprint matches the factory description: **2.0 m (X) × 2.0 m (Y) ×
2.0 m (Z)** envelope, centred at station origin (S01 at world `[2.5, 6.0, 0.0]`).

| Element | X | Y | Z / height | Notes |
|---------|---|---|-----------|-------|
| Table frame footprint | 1.6 | 0.8 | — | back-set within envelope |
| Work height (top surface) | — | — | 0.90 | ergonomic standing height |
| Worktop thickness | — | — | 0.06–0.08 | with apron |
| Back uprights above top | — | — | 0.70 | carry shelf/HMI |
| Angled bin (each) | 0.18–0.22 | 0.14–0.16 | 0.12 | tilted 15–20° |
| Kit box (each) | 0.34 | 0.34 | 0.34 | 6–10 units, stacked ≤2 layers |
| Pallet (each) | 0.9 | 0.75 | 0.12 | EUR-ish proportion |
| Pallet zone marking | 1.9 | 1.3 | 0.02 | flat on floor |
| Outfeed conveyor | 1.25 (len) | 0.60 | 0.40 (belt top) | line centre y = 6.0 |
| Control panel / HMI | 0.5 | 0.15 | 0.7 (body) | screen ~0.36 × 0.28 |
| E-stop | 0.16 | 0.05 | mounted ~1.1–1.2 | red mushroom Ø 0.04 |
| Stack light | Ø 0.06 | — | 0.30 (3 segments) | on an upright |
| Task light bar | 0.9 | 0.15 | 0.06 | ~2.0–2.2 above floor |
| Safety stripe | 2.0 | 0.10–0.15 | 0.02 | walkway edge |
| Info panel board | 1.2 | 0.05 | 0.7 | at `[2.5, 8.6, 1.6]`, faces +Y |
| Info trigger zone | 2.2 | 1.6 | 2.2 | in front of info panel |

Clearances: keep a ≥1.0 m operator standing zone on the +Y (walkway) side and a
clear aisle so the avatar can pass; nothing may intrude into the walkway at
y = 10.5.

---

## 9. Human interaction

- **Primary user:** one loading operator, standing, working the +Y side of the
  bench.
- **Reach zones:** bins and worktop within a 0.5 m comfortable reach arc; HMI at
  eye-to-chest height, angled ~10–15° toward the operator.
- **Ergonomics:** 0.90 m work height for standing tasks; toe clearance under the
  table; rounded worktop front edge; no sharp exposed profile ends (slot covers
  and end caps present).
- **Manual actions implied by the model:** lifting from pallet → placing into
  bins/trays → pushing tray onto conveyor → pressing kit-confirm on HMI.
- **Avatar (Unity) interaction:** the walkthrough avatar approaches from the
  walkway, the info trigger fires, and the info panel presents the station
  description. The station reads clearly as "manual input point" even without
  a visible human.

---

## 10. Safety equipment

- **Emergency stop:** red mushroom button on a yellow backing plate, reachable
  from the operator position, wired (visually) into the cell safety chain.
- **Stack light (signal beacon):** 3-segment red/amber/green on a pole above the
  bench for at-a-glance status.
- **Floor markings:** yellow walkway-edge stripe and a defined pallet-zone
  outline; a subtle black/yellow hazard hint at the conveyor pinch point.
- **Conveyor guard:** a small fixed side guard at the outfeed transfer/pinch.
- **Edge safety:** chamfered edges, profile end caps, no protruding bolts on
  operator-facing surfaces.
- **Labelling:** safety pictograms near the e-stop and conveyor (see §12).

There is **no light curtain or full fence** here (that belongs to the robot cell,
S03); the loading station is intentionally open and low-risk.

---

## 11. Electrical equipment

Represent as believable industrial detail (mostly visual; no wiring simulation):

- **Control cabinet:** a compact powder-coated enclosure under/beside the bench
  with a hinged door, latch, and a small cable gland plate — the Rittal/Siemens
  cabinet idiom.
- **PLC / IO:** implied inside the cabinet; optionally a DIN-rail strip visible
  through a small window with Beckhoff-style bus-terminal blocks (slim, colour-
  coded coupler + terminals).
- **HMI:** a small wall/arm-mounted touch panel (Siemens/Beckhoff panel look),
  dark glass front, thin bezel, one hardware button row.
- **Energy chain & trunking:** a black cable drag chain along one upright and
  slotted cable duct routing to the cabinet.
- **Pneumatics:** a Festo-style FRL unit + a couple of blue/black air lines to
  the conveyor drive or a simple pusher.
- **Power indicator:** a small green "power on" indicator on the cabinet.

Keep all of this as low-poly proxy shapes; the *silhouette and colour* sell the
realism, not internal detail.

---

## 12. Labels

Labels are what make an industrial station read as real. Provide as decals /
small text planes (baked or as simple textured quads):

- **Station ID plate:** `S01 · LOADING` on the frame, brushed-metal plate look.
- **Info panel headline:** "Loading Station" + body describing kitting/outfeed
  (already provided via `INFO_Loading_Panel`).
- **Safety pictograms:** e-stop symbol, "mind your hands" pinch-point icon,
  ESD-sensitive-area symbol near the worktop.
- **Bin labels:** small part-number/kanban cards on each bin front.
- **Cabinet labels:** voltage warning (⚡) and a small nameplate.
- **Directional arrow:** a flow arrow on the conveyor guard pointing toward S02.
- **Manufacturer-style logo block:** a neutral, invented brand mark (do **not**
  use real logos) as a small badge on the frame.

Text should be legible at avatar reading distance (~1–2 m); keep font simple
sans-serif, high contrast (black on white / white on blue).

---

## 13. Lighting

- **Task light:** a slim LED bar under the bin shelf / on the back rail, throwing
  even light on the worktop (cool white ~5000 K feel). Model as a thin emissive
  bar plus a real area light in Blender for the review render.
- **Stack light:** emissive segments (only the active segment strongly emissive).
- **HMI glow:** faint self-illumination from the screen.
- **Scene lighting (review only):** a soft key (sun/area) plus low ambient so
  surfaces read without blowing out; neutral grey world background.
- **Unity note:** emissive materials should carry an emission channel that Unity
  can pick up; real Blender lights are for the review render and are not required
  in the exported station (Unity provides scene lighting).

---

## 14. Surface finish

- **Aluminium profile:** brushed/anodised, medium roughness (0.30–0.40), subtle
  anisotropy acceptable but not required; matte, not mirror.
- **Powder coat:** fine orange-peel micro-texture, roughness ~0.4–0.5, no
  specular hotspots.
- **Laminate worktop:** low sheen, roughness ~0.55, faint linear grain.
- **Polymer accents:** semi-gloss, roughness ~0.35–0.45.
- **Rubber/ABS:** high roughness (0.85–0.95), soft matte.
- **Wear realism:** very light edge wear on pallets and conveyor rollers; the
  bench itself stays clean (medical context). Avoid heavy grunge — this is a
  modern, well-kept line.
- **Bevels:** every hard structural edge gets a small chamfer/bevel so highlights
  catch believably (see §16).

---

## 15. Manufacturing realism

Details that signal "this could be built":

- **Slot-profile framing** with visible T-slots, end caps and cast/stamped corner
  brackets; fasteners only where real ones would be (and mostly hidden).
- **Levelling feet** with hex bases and rubber pads.
- **Conveyor** built from a profile frame, side rails, and a series of rollers or
  a belt with a drive-end pulley and a small geared motor block.
- **Cabinet** with a door, hinge line, latch and gland plate.
- **Cable management** that actually goes somewhere (chain → duct → cabinet).
- **Consistent panel gaps** and repeated module spacing (profiles on a grid).
- **Kanban/label cards, pictograms and an ID plate** as described in §12.

The station should look **assembled from catalogue-style modules**, which is
exactly how Rexroth/Festo/ABB/Siemens/Beckhoff cells are actually specified.

---

## 16. Blender modelling notes

Guidance for the generator (still **no code here**):

- **Coordinate system:** metres, Z-up; keep station centred at S01 world
  `[2.5, 6.0, 0.0]`; front (operator/walkway) side is **+Y**.
- **Object hierarchy:** one `STATION_01_Loading_Root` empty; parent all parts to
  it; sub-assemblies (table+legs, conveyor+frame, panel+screen) parented with
  preserved world transform (set `matrix_parent_inverse`).
- **Reuse helpers:** build from `common_blender_utils` primitives
  (`create_cube`, `create_cylinder`, `add_bevel_modifier`, `shade_smooth`,
  `create_control_panel`, `create_emergency_stop`, `create_info_panel`,
  `create_warning_floor_marking`, `create_simple_conveyor`,
  `create_trigger_zone`).
- **Bevels:** apply `add_bevel_modifier` (≈0.01–0.03) to all box edges for
  realistic highlights; `shade_smooth` cylinders (rollers, buttons, posts).
- **Profiles:** approximate slot-profile as beveled boxes; optionally a shallow
  groove on show faces via a thin inset box, but only if the poly budget allows.
- **Bins:** tilt ~15–20° about X; alternate accent/neutral fronts.
- **Labels:** as thin textured quads or converted text meshes (text objects do
  not export to glTF — convert to mesh, as the info panel already does).
- **Naming:** follow the WP B convention strictly (`STATION_*`, `PHYS_*`,
  `COLLIDER_*`, `TRIGGER_*`, `INFO_*`) — see §5.
- **Materials:** create once, reuse; map to the palette in §6.

---

## 17. Performance constraints

- **Poly budget (whole station):** aim for **≤ 15–20 k triangles**; this is a
  walkthrough asset seen at close range but must scale to a full 7-station line.
- **Primitives:** low segment counts — cylinders 12–24 sides (buttons/rollers 12,
  larger rollers ≤24); avoid subdivision surfaces.
- **Instancing:** reuse identical parts (rollers, bins, boxes, feet, fasteners)
  via linked duplicates / shared mesh data where possible.
- **Modifiers:** keep bevels at low segment counts (1–2); apply on export.
- **Materials:** a small shared material set (≤12) across the whole line; no
  per-object unique materials.
- **Textures:** prefer solid PBR values; if decals/labels use textures, keep them
  small (≤512²) and atlas where feasible.
- **No real-time physics geometry bloat:** colliders are simple proxy boxes, not
  the visual mesh.

---

## 18. Unity considerations

- **Export:** glTF **.glb**, Y-up, `+Y` forward mapping handled on export; apply
  transforms; scale 1.0 (1 Blender m = 1 Unity m).
- **Custom properties → glTF extras:** carry `unity_tag`, `station_id`,
  `station_type`, and physics flags (`collider`, `collider_type`, `rigidbody`,
  `mass`, `kinematic`, `is_trigger`) so a Unity import script can add the right
  components.
- **Colliders:** static box colliders on table, pallets, conveyor frame, cabinet,
  uprights; a **trigger** (`TRIGGER_Info_Loading`) for the info event.
- **Rigidbodies:** kit boxes (`PHYS_Loading_Box_*`) flagged as movable rigid
  bodies (mass ~0.5 kg) for optional avatar interaction; everything else static.
- **Pivots:** station root pivot at the floor footprint centre; part pivots sane
  for any future articulation (e.g., cabinet door hinge, conveyor rollers).
- **Emissive:** stack-light segments, HMI screen and task bar use emission so
  they glow in Unity without extra lights.
- **Naming for scripting:** prefixes let Unity find/group objects (`STATION_`,
  `CONVEYOR_`, `PHYS_`, `COLLIDER_`, `TRIGGER_`, `INFO_`).
- **LOD (optional/future):** the low-poly build can serve as LOD0; a decimated
  LOD1 could be generated later if the full line needs it.

---

### Design references (aesthetic language only — nothing copied)

- **Bosch Rexroth** — aluminium slot-profile structural framing, workstation
  ergonomics, cable/energy-chain routing.
- **Festo** — pneumatics (FRL units, blue/black tubing), clean blue-grey product
  language, compact actuators.
- **ABB** — robust powder-coated structures, safety-yellow accents, industrial
  robustness cues.
- **Siemens** — HMI/panel and cabinet aesthetic, signal-blue accent register,
  status/stack-light conventions.
- **Beckhoff** — slim DIN-rail bus terminals and controller styling for the
  electrical detail.

This specification describes a **generic modern industrial loading station** in
that shared visual language and does not reproduce any specific commercial
product.
