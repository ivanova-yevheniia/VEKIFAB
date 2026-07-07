# WP B — Multi-Agent Station Review Orchestrator

A reusable review pipeline that hardens any VEKIFAB station (S01–S07) to
"Bosch-internal-demo / digital-twin" quality by running a full **AI Engineering
Organization** (see `ENGINEERING_ORGANIZATION.md` and `organization_chart.json`)
over a single station spec. Roles run **sequentially**; each sees the accumulated
model plus all prior reports, applies only what its discipline owns, rebuilds, and
validates.

> The agents never invent a new renderer. They only edit the two JSON specs that
> drive the geometry and then rerun the existing procedural builder.

---

## What each agent may touch (pipeline contract)

- **Edit only** (and only the disciplines authorised in each profile /
  `organization_chart.json`):
  - `parametric_specs/<station>_parameters.json` — the component tree.
  - `parametric_specs/<station>_assembly.json` — build ops + dependency graph
    (kept consistent with the parameter file).
- **Never edit:** `procedural_builder/`, `generators/`, the canonical
  `material_library`, `design_specs/factory_style_guide.md`, or the top-level repo
  structure.
- **Authority:** `factory_style_guide.md`, `industrial_rules.json`,
  `manufacturing_constraints.json`, `agents/review_checklist.json`,
  `agents/organization_chart.json`.

Hard limits every agent inherits: canonical palette only (**≤16 materials**),
**≤20 000 triangles** (target 15 000), single station root, WP B naming prefixes,
colliders as box proxies, glb Y-up.

---

## Run order (0 → 14) and role mapping

**File-prefix ≠ run-order.** A profile's numeric prefix is a stable role ID; the
step number below is its position in this run. Integration (role 11) runs before
CTO (role 10) by design.

| Step | Role ID / profile | Department | Modifies model? |
|------|-------------------|------------|-----------------|
| 0  | `00_chief_engineer`               | Management  | No (writes plan) |
| 1  | `01_mechanical_engineer`          | Engineering | **Yes** |
| 2  | `02_manufacturing_engineer`       | Engineering | **Yes** |
| 3  | `03_electrical_engineer`          | Engineering | **Yes** |
| 4  | `04_pneumatic_engineer`           | Engineering | **Yes** |
| 5  | `05_maintenance_engineer`         | Engineering | **Yes** |
| 6  | `06_safety_engineer`              | Engineering | **Yes** |
| 7  | `07_ergonomics_engineer`          | Engineering | **Yes** |
| 8  | `08_industrial_designer`          | Design      | **Yes** |
| 9  | `09_factory_operator`             | Quality     | Flags (rarely) |
| 10 | `11_integration_engineer`         | Management  | **Yes** (conflicts only) |
| 11 | `12_quality_assurance_inspector`  | Quality     | No (punch list) |
| 12 | *punch-list fix loop*             | Engineering/Design | **Yes** (owning agents) |
| 13 | `10_cto_reviewer`                 | Management  | Integration-level only |
| 14 | `13_customer_representative`      | Management  | No (acceptance) |

Rationale: **plan** first, then structure/load paths, then how it is made, then
how it is powered/piped, then serviced, then safety and the human, then the visual
system, then the voice-of-user, then **integrate**, then **inspect**, then **fix**,
then **gate**, then **accept**.

---

## Per-step loop (the 7 core actions)

For each step:

### 1. Read the station specs
Read `parametric_specs/<station>_parameters.json` and `<station>_assembly.json`,
the governing docs above, and this role's profile in `agent_profiles/`. Open the
latest `exports/screenshots/<station>.png` if useful.

### 2. Read previous agent reports (and the plan)
Read `review_outputs/00_engineering_plan_<station>.md` and every existing
`review_outputs/*_<station>.md` (in run order). **Do not overturn a prior accepted
change** without recording a `## Conflict` block for the Integration Engineer.

### 3. Apply only discipline-specific improvements
Using the profile's *allowed / forbidden changes*, make the smallest change that
answers a failed review question. Keep the assembly file in sync (new named
objects that need cross-part parenting get an operation or join an existing one).
**Add only functional detail a real machine requires — no decoration.** Preserve
layout unless the profile explicitly authorises an orientation/pose fix.

### 4. Write the report
Write `review_outputs/<role_id>_<station>.md` (e.g. `01_mechanical_S04.md`,
`12_qa_punchlist_S04.md`) using the sections in `review_checklist.json`. Score all
categories for context; you are accountable for the ones your profile owns.

### 5. Rebuild the station (only after a modifying step)
```bash
cd B_Blender/procedural_builder
blender --background --python builder.py -- \
  ../parametric_specs/<station>_parameters.json \
  ../parametric_specs/<station>_assembly.json \
  ../parametric_specs/manufacturing_constraints.json \
  ../parametric_specs/industrial_rules.json
```
Outputs refresh in `exports/{blend,glb,screenshots}/<station>.*`. Non-modifying
steps (0, 9-when-flag-only, 11 QA, 14 Customer) skip the rebuild.

### 6. Run validation — **continue only if errors == 0**
The build is complete for the step only when:
- **0 errors** (warnings triaged and explained),
- **triangles ≤ 20 000** (headless tri-count pass on the `.blend`),
- **≤16 materials**, all canonical palette keys,
- required colliders / triggers / rigidbodies present with correct names.

If any check fails, fix within the step's scope and rebuild. If the fix is out of
scope, log a finding for the owning agent and revert the change. **Do not proceed
to the next step while errors > 0.**

### 7. Continue to the next step
Leave the model building and validated. The next role starts at action 1.

---

## Stage specifics

- **Step 0 — Chief Engineer:** writes `00_engineering_plan_<station>.md` (focus
  areas + acceptance bar). No model change, no rebuild.
- **Step 10 — Integration Engineer:** resolves every recorded `## Conflict` by the
  ladder below, verifies no subsystem broke another, then rebuilds/validates.
- **Step 11 — QA Inspector:** produces `12_qa_punchlist_<station>.md` with items
  `PL-n` (critical/major/minor) each assigned to an owning agent. Does **not** fix.
- **Step 12 — Fix loop:** the orchestrator routes each open punch-list item to its
  owning agent (01–08), which applies the fix within its scope, rebuilds and
  validates. Repeat until no `critical`/`major` items remain, then re-run QA if
  needed.
- **Step 13 — CTO:** final gate; integration-level fixes only; writes the
  aggregate verdict.
- **Step 14 — Customer Representative:** writes `13_customer_acceptance_<station>.md`;
  ACCEPT / ACCEPT_WITH_CONDITIONS / REJECT. On reject, loop back to Step 0 for a
  new iteration.

---

## Conflict hierarchy

When two disciplines' ideal changes collide, the higher wins:

```
safety > mechanical integrity > maintenance > electrical/pneumatics >
ergonomics > manufacturing > visual design > presentation
```

The losing agent records a `## Conflict` block; the **Integration Engineer**
applies the ladder and implements the reconciling edit; the **CTO** ratifies. A
**safety** finding is never traded away — it is resolved in safety's favour or the
station FAILs.

---

## Station PASS rule

`PASS` requires: no owned checklist category below its threshold, **no open
`blocker`/`critical`/safety finding**, punch list clear of critical/major items,
0 build errors, triangles ≤ 20 000, and a Customer decision of ACCEPT (or
ACCEPT_WITH_CONDITIONS with the conditions logged).

---

## Reusability across stations

Nothing here is S01-specific. To review another station, pass its `<station>_*`
spec pair through the same loop; the org chart, profiles and checklist are shared
across S01–S07.

### One-line invocation pattern (per step)

```
Act as agent_profiles/<role_id>.md. Review <station_id>. Follow the 7-action loop
in orchestrator.md. Read the engineering plan + prior reports, edit only your
discipline's spec nodes, rebuild, validate (errors==0), and write
review_outputs/<role_id>_<station_id>.md.
```
