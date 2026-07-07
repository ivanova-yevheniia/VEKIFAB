# procedural_builder — Generic Procedural Station Renderer (WP B)

This package turns Blender into a **pure procedural renderer**. It knows nothing
about loading stations, assembly stations, robot cells, vision, packaging or
storage. It understands only **generic components** (box, cylinder, roller,
frame, panel, label, light, cabinet, beam, profile, conveyor, shelf, text,
empty, …) and builds whatever a set of JSON specifications describes.

> **Goal:** future stations (S02, S03, S04, …) are produced by writing new JSON
> only. **No new Python is required.**

---

## The pipeline

```
parametric_specs/<name>_parameters.json   ── geometry parameters (what to build)
parametric_specs/<name>_assembly.json     ── ordered build ops + dependency graph
parametric_specs/manufacturing_constraints.json ── engineering limits (validate)
parametric_specs/industrial_rules.json    ── global rules & defaults
                     │
                     ▼
          procedural_builder/builder.py   ── one entry point
                     │
     ┌───────────────┼───────────────────────────────┐
     ▼               ▼                                 ▼
material_engine   scene_builder ── component_registry ── geometry_builder
 (create/reuse     (walk params,     (type → builder)     (bpy primitives)
  materials)        resolve layout)
                     │
                     ▼
              assembly_engine   ── topological build order + cross-part parenting
                     │
                     ▼
                 validation     ── static (specs) + runtime (built scene)
                     │
                     ▼
        exports/blend/*.blend · exports/glb/*.glb · exports/screenshots/*.png
```

---

## Modules

| File | Responsibility |
|------|----------------|
| `geometry_builder.py` | Low-level, generic Blender primitives: box, cylinder, empty, text-mesh, light, plus bevel/smooth/rotation/material/Unity-flag/parent helpers. Holds **no dimensions**. |
| `component_registry.py` | Maps a generic component *type* → builder function. Extensible at runtime via `register(...)`. Aliases (cube/beam/profile/frame/panel/shelf/cabinet/conveyor → box; roller/post/pole → cylinder; label/text → text-mesh). |
| `material_engine.py` | `MaterialEngine.get(name)` creates a material once from the JSON `material_library` and **reuses** it thereafter. Never duplicates materials. |
| `scene_builder.py` | Reads `*_parameters.json`, walks the component tree with a small generic **node grammar**, resolves names/positions/materials, and creates every object. Applies `industrial_rules` defaults. |
| `assembly_engine.py` | Reads `*_assembly.json`, topologically sorts operations by `dependencies`, and attaches each operation's primary object to its declared `parent` (preserving world transform). |
| `validation.py` | Static + runtime checks (see below). Returns a `Report` of errors/warnings. |
| `builder.py` | Single entry point `build_station(parameter_file, assembly_file, constraints_file, rules_file)` and a CLI that auto-discovers spec pairs. |

---

## The node grammar (what `scene_builder` understands)

Everything is generic; none of it is station-specific.

- **Node** — any dict with a `primitive`. Produces one object, or `count`
  objects when combined with a layout:
  - `offsets_m` — explicit list of `[dx,dy,dz]` (relative to station origin)
  - `start_offset_m` + `step_m` — linear array
  - `stack` — layered grid (`grid_offsets_m`, `layers`, heights, jitter)
  - **inherited** — reuse a sibling array's `offsets_m` of matching `count`
- **Position** — `world_position_m` (absolute) · `offset_m` (origin + offset) ·
  `offset_from_parent_m` (parent-local) · `start_world_m`/`end_world_m` midpoint.
- **Container** — a dict without `primitive`. Its `naming` is applied to its
  *primary* child; other children parent to that primary. Primary selection:
  an explicit `"primary": true`, else a generic component-role hint, else the
  first primitive.
- **Materials** — `material` (single) or `material_cycle` (per-instance list),
  keyed into `material_library`.
- **Items** — a node with an `items` list builds each item as a label.
- **Light** — a dict with `type` in {AREA, POINT, SUN, SPOT} builds a light.
- **Flags** — `collider`, `rigidbody`, `is_trigger`, `unity_tag`, `display`,
  `hide_render`, `bevel_m`, `rotation_deg`/`tilt_deg`, `axis` — all generic.

---

## Validation (`validation.py`)

**Static** (no Blender): unknown component types · missing materials · duplicate
names · missing dependencies · parent/dependency loops · invalid hierarchy ·
missing transforms.

**Runtime** (in Blender): missing objects/transforms · duplicate names · parent
loops in the built hierarchy · overlapping bounding boxes (flat markings,
triggers and floors are skipped generically).

`build_station()` runs the static pass **before** building and the runtime pass
**after**, and prints a `Report` summary.

---

## Running it

Auto-discover every `*_parameters.json` + `*_assembly.json` pair in
`../parametric_specs`:

```bash
blender --background --python builder.py
```

Build one explicit station:

```bash
blender --background --python builder.py -- \
    ../parametric_specs/<name>_parameters.json \
    ../parametric_specs/<name>_assembly.json \
    ../parametric_specs/manufacturing_constraints.json \
    ../parametric_specs/industrial_rules.json
```

Outputs land in `../exports/{blend,glb,screenshots}/<name>.*` (the `<name>` is
derived from the parameter filename — no station name is hardcoded).

---

## Adding a new station — **no Python**

1. Have the Design Agent + Parametric Agent produce, in `parametric_specs/`:
   - `<station>_parameters.json` (components, `material_library`, station meta)
   - `<station>_assembly.json` (ordered operations + dependencies)
2. Reuse the shared `manufacturing_constraints.json` and `industrial_rules.json`
   (or provide station-specific variants).
3. Run `builder.py`. Done.

If a station needs a genuinely new **generic** primitive (something no existing
type can express), register it once:

```python
import component_registry as registry

@registry.register("my_new_generic_type")
def build_my_type(ctx, name, node, center, rotation_deg, material_key, parent):
    ...
```

That is the *only* circumstance under which Python changes — and even then it is
a generic component, never a station.

---

## Design guarantees

- **No station knowledge in code** — grep the `.py` files: no `Loading`, `S01`,
  `Pallet`, `Workbench`, `Assembly`, `Robot`, etc.
- **No hardcoded geometry** — every dimension, offset, name, material and step
  comes from JSON; defaults (cylinder segments, bevel segments) come from
  `industrial_rules.performance_rules`.
- **Materials are never duplicated** — created once per name and reused.
- **Deterministic hierarchy** — intra-component parenting from the parameter
  tree, cross-component attachment from the assembly graph, all with preserved
  world transforms.
- **Unity-ready** — colliders/rigidbodies/triggers/tags exported as glTF
  `extras`; glb is Y-up.

---

## Verified

Built end-to-end in Blender 5.1 from the Loading Station specs: **61 objects,
0 errors, 0 warnings**, producing `exports/{blend,glb,screenshots}/loading_station.*`.
The renderer received the specs only — it was never told what a "loading
station" is.
