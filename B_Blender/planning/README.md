# planning — AI Factory Planner

The first VEKIFAB component that **makes engineering decisions**. Instead of a
fixed 7-station sequence, the planner reads a customer's requirements and decides
**which stations the line needs**, then explains every choice.

**Standard library only. Deterministic. No Blender. `procedural_builder` untouched.**

## Files
- `planner.py` — the planner (reads `customer_requirements.json` → writes
  `production_line_plan.json` + `planner_decisions.md`).
- `planning_rules.json` — thresholds, gates and the station catalog.
- `planning_examples/` — ready-to-run example requirement sets, each producing a
  **different** factory layout.

## What it reasons about
Daily production · automation level · available floor area · workers · quality
requirements · budget.

## Decision logic (from `planning_rules.json`)
| Station | Included when |
|---------|---------------|
| Loading / Assembly / Packaging / Storage | always (core) |
| **Robot handling cell** | automation = full **or** daily output ≥ 500 — **and** budget ≥ medium **and** area ≥ 120 m² |
| **Vision inspection** | quality mentions optical/vision/high **or** regulated |
| **Functional test** | quality mentions functional/electrical/test **or** regulated |
| **Parallel assembly** (×N) | throughput exceeds one station's capacity (N = ceil(output ÷ capacity)) and budget ≥ medium |
| **Compact layout** | floor area ≤ 150 m² |

Example reasoning: *low automation → no robot cell*; *high automation → robot cell*;
*high quality → vision inspection*; *high throughput → parallel assembly*; *small
factory → compact layout*.

## Run
```bash
# one requirement set
python planner.py planning_examples/02_medical_full_line/customer_requirements.json

# batch: every example
python planner.py
```

## Example outcomes (all different)
| Example | Stations | Robot | Vision | Test | Assembly | Layout |
|---------|----------|-------|--------|------|----------|--------|
| 01 micro manual workshop | 4 | – | – | – | ×1 | compact |
| 02 medical full line | 7 | ✓ | ✓ | ✓ | ×2 | standard |
| 03 high-throughput automated | 7 | ✓ | ✓ | ✓ | ×4 | standard |
| 04 budget prototype | 5 | – | ✓ | – | ×1 | standard |
| 05 high-quality low-volume | 6 | – | ✓ | ✓ | ×1 | standard |
| 06 compact automated cell | 6 | ✓ | ✓ | – | ×1 | compact |

## Outputs
- `production_line_plan.json` — pipeline-compatible line plan (stations with
  type/purpose/equipment/position, conveyors, and a `planner` metadata block). It
  feeds the downstream `requirements → parametric_specs → asset composition →
  procedural_builder` flow.
- `planner_decisions.md` — an inputs table plus a decision table (result · rule ·
  rationale) and the resulting station flow.

## Pipeline position
```
customer_requirements.json
        │   planning/planner.py   ← decides the line
        ▼
production_line_plan.json → factory_description → parametric_specs → asset composition
        → procedural_builder → Blender → Unity avatar walkthrough
```
