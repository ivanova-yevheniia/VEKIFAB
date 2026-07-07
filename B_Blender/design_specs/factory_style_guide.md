# VEKIFAB Factory — Industrial Design Style Guide

**Status:** Single source of truth for the visual and structural design of **every**
VEKIFAB station (S01–S07) and every reusable asset.
**Scope:** Work Package B (Blender generation → Unity walkthrough).
**Rule of thumb:** *If it does not follow this guide, it does not ship.* Every
station generator, parametric spec and asset must conform so the whole line reads
as **one modern smart factory**.

Related sources this guide governs and unifies:
`parametric_specs/industrial_rules.json` · `parametric_specs/*_parameters.json` ·
`assets/*` + `assets/asset_registry.json` · `procedural_builder/` ·
`design_specs/loading_station_design.md`.

---

## 1. Overall design philosophy

- **Modern, clean, medical-adjacent.** The plant builds a compact medical infusion
  pump; surfaces read as tidy, well-lit, maintainable and calm — never grimy.
- **Assembled from catalogue modules.** Everything looks specified from a
  structural-framing catalogue: aluminium profile frames, bolt-on panels, standard
  conveyors, standard control gear. Realism comes from *system consistency*, not
  from unique hero geometry.
- **Rectilinear + restrained.** Orthogonal forms, small consistent chamfers, one
  accent colour, safety colours only where functional.
- **Legible at walkthrough distance.** The avatar reads the line at 1–3 m; the
  silhouette, colour and labels must communicate each station's function instantly.
- **Function first.** Every visible element implies a real function (guide, guard,
  route, signal, service). No decorative clutter.

---

## 2. Industrial inspiration (language only — nothing copied)

The line speaks the shared visual language of modern automation, **without
reproducing any specific product or logo**:

| Domain | Inspiration (aesthetic language only) |
|--------|----------------------------------------|
| Structural framing | Bosch Rexroth, item, Festo slot-profile systems |
| Pneumatics & clean product form | Festo (FRL units, blue/black tubing, blue-grey register) |
| Robotics & robustness | ABB (powder-coated masses, safety-yellow accents) |
| HMI / control / signalling | Siemens (SIMATIC panels, signal-blue, stack-light conventions) |
| Bus terminals / controllers | Beckhoff (slim DIN-rail terminal styling) |
| Enclosures | Rittal, Eldon (RAL-grey powder-coated cabinets) |
| Conveyors | Interroll, Dorner (frame + bright rollers) |
| Guarding | Axelent, Troax, Satech (yellow posts + mesh) |
| Signal towers | Patlite, Werma (red/amber/green) |
| Cable management | igus, Kabelschlepp (black articulated e-chain) |
| Sensors | SICK, Cognex, Keyence (dark housings, red windows) |

Invented, neutral brand marks only — **never** a real company logo.

---

## 3. Material palette

The **canonical material set** (shared across the whole line; ≤16 materials total).
Keys and PBR values are authoritative — mirror `material_library` in the parametric
specs and asset `parameters.json`.

| Key | Use | Base color (lin) | Metallic | Roughness | Notes |
|-----|-----|------------------|----------|-----------|-------|
| `metal_light` | Aluminium profile, rollers, bright metal | 0.70, 0.72, 0.75 | 0.9 | 0.35 | brushed/anodised, matte |
| `metal_dark` | Feet, brackets, frames, conveyor frame | 0.15, 0.15, 0.17 | 0.9 | 0.40 | powder-coat charcoal |
| `worktop_grey` | ESD worktops | 0.82, 0.83, 0.85 | 0.0 | 0.55 | low-sheen laminate |
| `white_panel` | Info boards, light panels | 0.90, 0.90, 0.92 | 0.0 | 0.50 | matte white |
| `blue_accent` | Accent trims, bin fronts, HMI bezel | 0.10, 0.35, 0.75 | 0.1 | 0.40 | the single accent |
| `safety_yellow` | Floor/edge markings, e-stop plate, fence posts | 0.95, 0.80, 0.05 | 0.0 | 0.60 | safety only |
| `warning_black` | Hazard stripes, label text, domes | 0.03, 0.03, 0.03 | 0.0 | 0.70 | deep matte |
| `rubber_black` | Feet pads, roller lagging, cable chain | 0.05, 0.05, 0.05 | 0.0 | 0.90 | soft matte |
| `cardboard` | Kit trays, cartons | 0.58, 0.42, 0.26 | 0.0 | 0.85 | kraft brown |
| `wood_pallet` | Pallets | 0.55, 0.40, 0.24 | 0.0 | 0.75 | pale timber |
| `screen_dark` | HMI / display glass | 0.02, 0.02, 0.03 | 0.0 | 0.20 | emissive ~1.0 |
| `led_red` | E-stop button, fault segment | 0.80, 0.05, 0.05 | 0.0 | 0.40 | emissive ~3.0 |
| `led_amber` | Warning segment | 0.95, 0.63, 0.05 | 0.0 | 0.40 | emissive ~3.0 |
| `led_green` | OK segment, power indicator | 0.05, 0.80, 0.20 | 0.0 | 0.40 | emissive ~3.0 |
| `led_white` | Task-light strip | 0.95, 0.96, 1.00 | 0.0 | 0.30 | emissive ~2.5 |

**Rules:** create each material **once** and reuse; never duplicate; emission is
reserved for screens, status LEDs and task lights only.

---

## 4. Color palette

Governed by the **60 / 30 / 10** rule (from `industrial_rules.json`):

- **~60 % neutral metal** — `metal_light` structure.
- **~30 % darker structure + worktops** — `metal_dark`, `worktop_grey`.
- **~10 % accent** — `blue_accent` (≤15 % of any surface).
- **Safety colours are *outside* the budget** — `safety_yellow` + `warning_black`
  are functional, used only for markings, e-stops, fences.

| Role | Hex (approx) |
|------|--------------|
| Primary structure | `#B4B7BF` |
| Secondary structure / worktop | `#26262B` / `#D2D3D6` |
| Accent | `#1A59BF` |
| Safety | `#F2CC0D` |
| Hazard contrast | `#080808` |
| Status ok / warn / fault | `#0DCC33` / `#F2A20D` / `#CC0D0D` |
| Info board / text | `#E8E8EA` / `#111111` |

No rainbow surfaces. Value and roughness contrast carry the realism, not hue.

---

## 5. Standard aluminium profile system

- **Asset:** `aluminium_profile` — the universal structural member for every frame.
- **Section:** 40 × 40 mm default (options 20 / 40 / 45 / 80 mm). One line, one
  section family; do not mix arbitrarily.
- **Finish:** anodised matte (`metal_light`), visible T-slots, black slot covers on
  unused faces, end caps on exposed ends.
- **Work height:** worktops at **0.90 m** (standing). Uprights rise ~0.70 m above
  the worktop to carry shelves, HMI arms and signal towers.
- **Joints:** butt joints via corner brackets/gussets; panels bolt to `face_slot`
  faces. Every leg terminates in an `adjustable_foot`.
- **Grid:** members sit on a consistent module spacing; frames read as a repeated
  bay, not a one-off weldment.

---

## 6. Fasteners and structural details

- **No visible fasteners on operator/walkway-facing show faces.** Service fasteners
  live on the rear / `-X` side.
- Imply real construction: corner brackets, T-slot nuts (suggested), end caps,
  levelling feet with hex adjusters and rubber pads.
- **Every hard structural edge gets a small chamfer/bevel** (0.01–0.03 m) so
  highlights catch believably. Round parts (rollers, buttons, posts) are smooth-
  shaded.
- Consistent panel gaps; no interpenetrating geometry; nothing floats.

---

## 7. Conveyor style

- **Asset:** `roller_conveyor`.
- **Form:** powder-coated `metal_dark` frame + two side rails, a row of bright
  `metal_light` rollers, four legs, belt top at **0.40–0.45 m** (line centre y).
- **Rollers:** 16-sided cylinders on the **Y axis**; spacing regular; drive-end
  motor block hinted.
- **Flow:** left → right (**+X**); a `→ S0x` flow-arrow decal on the guard.
- **Colliders:** static box on the frame; belt plane collider for product.
  **Physics role:** `kinematic` (belt moves product; ~0.15 m/s).
- Guard the transfer/pinch points; hazard hint at the pinch.

---

## 8. HMI style

- **Asset:** `hmi_panel`.
- Dark `screen_dark` glass (subtle emission), a thin `metal_dark` bezel, one
  hardware button row in `blue_accent`.
- Mounted on a pole/arm at **1.20–1.45 m** centre height, tilted **−8° to −12°**
  toward the operator.
- One HMI per manned/automated station (S01, S02, S04, S05, S06). Collider: static.

---

## 9. Information panel style

- **Asset:** `information_panel`. **This is the avatar's read of the station.**
- White board (`white_panel`), **black high-contrast text**, on a `metal_dark` post.
- **Title** ~0.13 m + **body** ~0.06 m, body **word-wrapped to ~28 chars**.
- Board at **~1.6 m** centre height; **faces the walkway (+Y)** — the front is
  rotated 180° about Z so it reads from the aisle.
- Carries a **non-blocking trigger** (`TRIGGER_Info_*`) in front that fires the
  Unity info event.
- Text objects are **converted to mesh** (font objects don't export to glTF).
- Naming: board `INFO_<Station>_Panel`; trigger `TRIGGER_Info_<Station>`.

---

## 10. Stack light style

- **Asset:** `stack_light`.
- Base + short pole + **three emissive segments** bottom-to-top **red / amber /
  green** + a `warning_black` dome.
- Only the **active** segment reads strongly emissive.
- Mounted on a frame upright, top around **2.0–2.3 m**. One per station.

---

## 11. Emergency stop style

- **Asset:** `emergency_stop`.
- Red mushroom button (`led_red`) + black collar on a **`safety_yellow` backing
  plate**; faces outward toward the operator.
- **Reachable from the operator position** (≤0.8 m); present at every **manned**
  station (S01, S02, S03 cell, S04, S05, S06). Unmanned storage (S07) is exempt.
- Collider: static; Unity press event. Naming: `STATION_<nn>_<Name>_EStop`.

---

## 12. Cable routing style

- **Asset:** `cable_chain` (black articulated e-chain, `rubber_black`).
- Cables **always go somewhere**: e-chain → slotted duct → cabinet. **No free-
  hanging cables.**
- Pneumatics (where shown): a Festo-style FRL cluster at knee height with blue/black
  lines. Routing runs along one upright; supply on the `-X` service side.

---

## 13. Electrical cabinet style

- **Asset:** `electrical_cabinet`.
- RAL-grey powder-coat (`metal_light`) box, hinged door, latch handle
  (`metal_dark`), gland plate, a green `led_green` "power on" indicator, optional
  DIN-rail hint through a window.
- One per station (except S07). Door hinge available for articulation. Collider:
  static. Service access on the `-X` side; door swing ≥ 0.6 m clear.

---

## 14. Lighting style

- **Asset:** `task_light` — slim housing with a diffused **cool-white** LED strip
  (`led_white`) over worktops/inspection areas.
- In Blender a real area light may accompany the fixture **for review renders only**
  and is **excluded from glTF export** — Unity provides scene lighting.
- Emissive materials (screens, LEDs, task strips) carry an emission channel so they
  glow in Unity without extra lights. Neutral grey world for review renders.

---

## 15. Safety markings

- `safety_yellow` + `warning_black` **only** for safety; never decorative.
- **Emergency stop** at every manned station; **stack light** on every station.
- **Full fencing** (`safety_fence`) **only** for the robot cell (S03): yellow posts,
  grey mesh panels, bolt-down feet, one interlocked gate on the walkway side.
- Guard pinch points; chamfer edges; profile end caps; no sharp exposed ends.
- Safety pictograms near e-stops, pinch points and ESD zones.

---

## 16. Floor markings

- Thin flat `safety_yellow` decals (~0.02 m) at floor level.
- **Walkway edge stripe** along the aisle; **operator/work-zone** outline in front
  of manned benches; **pallet-zone** outline where pallets drop; **keep-out** hatch
  around the robot cell.
- Markings never block the walkway; the avatar aisle stays ≥ 1.2 m clear and the
  walkway centre (world y ≈ 10.5) is kept free of geometry.

---

## 17. Labels and typography

- **Font:** simple sans-serif, high contrast (black on white / white on blue).
- **Required per station:** an ID plate `S0x · NAME`, a conveyor **flow arrow**
  `→ S0(x+1)`, plus the info-panel title/body.
- Optional: bin kanban cards, cabinet voltage warning (⚡), ESD symbol.
- Readable at **1–2 m**. Text meshes only (converted from font); atlas label
  textures; **no real brand logos**.

---

## 18. Typical proportions

| Element | Value |
|---------|-------|
| Work height (worktop top) | 0.90 m |
| Uprights above worktop | ~0.70 m |
| Aluminium section | 40 × 40 mm |
| Conveyor belt top | 0.40–0.45 m |
| HMI centre height | 1.20–1.45 m, tilt −8…−12° |
| Info board centre | ~1.6 m, faces +Y |
| Stack light top | 2.0–2.3 m |
| Overhead clearance | ≥ 2.2 m |
| Walkway width | ≥ 1.2 m (aisle kept clear) |
| Operator standing zone | ≥ 1.0 m deep |
| Station spacing | footprints must not overlap; ≥ 0.75 m aisle between |

Units: **metres, Z-up** in Blender; exported **Y-up** for Unity (1 unit = 1 m).

---

## 19. Level of detail rules

- **Silhouette + colour first**; internal mechanism detail only where it reads at
  walkthrough distance.
- LOD importance by asset (see `asset_registry.json`): profiles/conveyors **high**
  (repeated); cabinets/HMI/fence **medium**; feet/bins/boxes/scanners/lights **low**.
- Approximate rather than model literally: T-slots as shallow insets, welded mesh as
  a thin panel, e-chain as a row of links, robot detail suggested not simulated.
- Low segment counts: cylinders 12 (buttons/small), 16 (rollers/medium), ≤24 (large);
  bevel segments ≤ 2; **no subdivision surface**.

---

## 20. Performance rules for Unity

- **Per-station triangle budget: target ~15 k, max ~20 k.** The full 7-station line
  must stay lightweight for a real-time avatar walkthrough.
- **Instance** identical parts (rollers, feet, boxes, bins, profiles, fasteners) via
  linked duplicates / shared mesh data.
- **Shared materials only** (≤16 across the whole line); no per-object unique
  materials; textures ≤ 512², atlas labels.
- **Colliders are simplified box proxies**, never the visual mesh.
- **Export:** glTF **.glb**, Y-up, apply transforms, scale 1.0, custom properties as
  `extras`. Review-only lights excluded. Pivot at footprint centre.
- Custom-property keys for Unity: `unity_tag`, `station_id`, `station_type`,
  `collider`, `collider_type`, `rigidbody`, `mass`, `kinematic`, `is_trigger`.

---

## 21. Blender modeling conventions

- **Units:** metres, Z-up; front (operator/walkway) side is **+Y**; flow is **+X**.
- **One root empty per station** (`STATION_<nn>_<Name>_Root`); parent all parts to
  it; preserve world transform on parenting (set `matrix_parent_inverse`).
- **Naming prefixes** (strict): `STATION_*`, `CONVEYOR_*`, `PHYS_*`, `COLLIDER_*`,
  `TRIGGER_*`, `INFO_*`. PascalCase names; instance suffixes `_1`, `_2`.
- Build from generic primitives via the procedural builder; bevel all box edges,
  smooth-shade round parts.
- Sub-assemblies (frame+legs, conveyor+rollers, panel+screen, cabinet+door,
  board+text) parent locally with preserved transforms.
- **No hardcoded geometry numbers in code** — everything flows from JSON specs.

---

## 22. Rules every station must follow

A station is **not compliant** unless all of the following hold:

1. Built on the **standard aluminium profile frame** at 0.90 m work height, on
   `adjustable_foot` levelling feet.
2. Uses **only the canonical material palette** (§3), obeying the 60/30/10 colour
   budget; safety colours only for safety.
3. Has **exactly one information panel** facing the walkway (+Y) with a title, a
   ≤28-char wrapped body, and a `TRIGGER_Info_*` volume.
4. Has **at least one safety asset** (stack light always; e-stop at every manned
   station; full `safety_fence` for the robot cell).
5. Connects to the line with a **`roller_conveyor`** (input and/or output) matching
   the `factory_description.json` topology; flow runs **+X**.
6. Carries an **electrical presence** (cabinet where applicable) and **routed
   cables** — no free-hanging wires.
7. Emits **status** via a stack light; uses **emissive** materials for screens/LEDs.
8. Includes the required **labels** (ID plate + flow arrow) in the standard
   typography.
9. Includes the required **floor/safety markings**; keeps the walkway (world
   y ≈ 10.5) and a ≥ 1.2 m aisle clear; footprint must not overlap neighbours.
10. Follows the **naming, hierarchy, collider/trigger and export conventions**
    (§20–21) so Unity import is automatic.
11. Stays within the **performance budget** (≤ ~20 k tris, shared materials,
    instanced repeats, simplified colliders).
12. Passes the **Factory Review** checks (`review/factory_review.py`) with no fail.

> Any new station generator, parametric spec or asset must cite and satisfy this
> guide. When this guide and a local spec disagree, **this guide wins** — update the
> spec, not the guide (unless the change is intentional and global).
